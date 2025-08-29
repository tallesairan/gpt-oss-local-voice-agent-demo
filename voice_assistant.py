import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import whisper
import openai
import subprocess, os, time, tempfile

# Configurar TTS para aceitar licença automaticamente
os.environ["COQUI_TOS_AGREED"] = "1"

# Importação para TTS
from TTS.api import TTS
from TTS.tts.configs.xtts_config import XttsConfig
from TTS.tts.models.xtts import Xtts
from TTS.utils.generic_utils import get_user_data_dir
from TTS.utils.manage import ModelManager

########################
# Konfiguration
########################
SAMPLERATE     = 16_000        # Hz
RECORD_SECS    = 4             # Länge einer Aufnahme
LLM_MODEL      = "gpt-oss-1"   # Modelo personalizado
WHISPER_MODEL  = "base"        # tiny / base / small / medium …
XTTS_MODEL     = "tts_models/multilingual/multi-dataset/xtts_v2"
XTTS_LANGUAGE  = "pt"          # Português
SYSTEM_PROMPT  = (
    "Você é um assistente útil. "
    "Interprete perguntas exclusivamente em português "
    "e responda sempre em português. "
    "Não use outros idiomas."
)

# Configurar o servidor personalizado da OpenAI
# Usando seu servidor que imita a API da OpenAI
openai.api_base = "https://gpt-proxy.ahvideoscdn.net/v1"
openai.api_key = "dummy-key"  # Chave dummy já que o servidor é seu

########################
# TTS initialisieren (einmalig, nicht in der Schleife!)
########################
# Carregar modelo XTTS V2 usando a API simplificada (fallback)
print("📥 Carregando modelo XTTS V2 (API simplificada)...")
tts = TTS(
    model_name=XTTS_MODEL,
    progress_bar=False,
    gpu=False,
)
print("✅ Modelo XTTS V2 carregado (API simplificada)!")

# Tentar preparar XTTS em modo low-level (como test_xtts_v2)
XTTS_LOWLEVEL_READY = False
xtts_model = None
try:
    print("📥 Preparando XTTS V2 (low-level)...")
    ModelManager().download_model(XTTS_MODEL)
    model_path = os.path.join(get_user_data_dir("tts"), XTTS_MODEL.replace("/", "--"))
    config = XttsConfig()
    config.load_json(os.path.join(model_path, "config.json"))
    xtts_model = Xtts.init_from_config(config)
    xtts_model.load_checkpoint(
        config,
        checkpoint_path=os.path.join(model_path, "model.pth"),
        vocab_path=os.path.join(model_path, "vocab.json"),
        eval=True,
        use_deepspeed=False,
    )
    # Não usar CUDA em ambiente local sem GPU
    XTTS_LOWLEVEL_READY = True
    print("✅ XTTS V2 low-level pronto!")
except Exception as e:
    print(f"⚠️ XTTS low-level indisponível, usando API simplificada. Motivo: {e}")


def say_text(text: str):
    """Gera áudio via XTTS. Usa low-level (inference_stream) quando disponível, senão fallback para API simplificada."""
    try:
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            tmp_path = tmp.name

        reference_audio = "reference_voice.wav"
        if not os.path.exists(reference_audio):
            print("📝 Criando arquivo de referência de voz...")
            create_reference_audio(reference_audio)

        if XTTS_LOWLEVEL_READY and xtts_model is not None:
            # Low-level: get_conditioning_latents + inference_stream
            print("🎵 [XTTS low-level] Processando referência...")
            gpt_cond_latent, speaker_embedding = xtts_model.get_conditioning_latents(audio_path=reference_audio)
            print("🎤 [XTTS low-level] Gerando áudio...")
            chunks = xtts_model.inference_stream(
                text,
                XTTS_LANGUAGE,
                gpt_cond_latent,
                speaker_embedding,
                repetition_penalty=2.5,
                temperature=0.6,
            )
            audio_chunks = []
            for chunk in chunks:
                chunk_np = chunk.detach().cpu().numpy().squeeze()
                # Converter para int16 para WAV
                chunk_i16 = (chunk_np * 32767).astype(np.int16)
                audio_chunks.append(chunk_i16)
            if audio_chunks:
                combined = np.concatenate(audio_chunks)
                wav.write(tmp_path, 24000, combined)
            else:
                raise RuntimeError("Nenhum áudio gerado pelo XTTS low-level")
        else:
            # Fallback: API simplificada
            print("🎤 [XTTS API] Gerando áudio...")
            tts.tts_to_file(
                text=text,
                language=XTTS_LANGUAGE,
                speaker=reference_audio,  # v2 aceita caminho WAV no speaker
                file_path=tmp_path,
                speed=0.8,
                temperature=0.6,
                repetition_penalty=2.5,
            )

        subprocess.run(["afplay", "-q", "1", tmp_path])
        os.remove(tmp_path)
        print(f"🔊 TTS: {text}")

    except Exception as e:
        print(f"❌ TTS Erro: {e}")
        # Fallback para macOS say
        try:
            subprocess.run(["say", "-v", "Samantha", "-r", "160", text])
        except Exception:
            pass


def create_reference_audio(filename: str):
    """Cria um arquivo de áudio de referência simples"""
    try:
        subprocess.run([
            "say",
            "-v", "Samantha",
            "-o", filename,
            "Olá, esta é minha voz de referência para o sistema de síntese de fala."
        ], check=True)
        print(f"✅ Arquivo de referência criado: {filename}")
    except Exception as e:
        print(f"❌ Erro ao criar arquivo de referência: {e}")

########################
# STT- & LLM-Funktionen
########################
# Carregar modelo Whisper uma vez (global)
print("📥 Carregando modelo Whisper...")
import warnings
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    whisper_model = whisper.load_model(WHISPER_MODEL)
print("✅ Modelo Whisper carregado!")

def record(seconds: int, sr: int = SAMPLERATE) -> str:
    print("🎙️  Fale agora...")
    audio = sd.rec(int(seconds * sr), samplerate=sr, channels=1, dtype='int16')
    sd.wait()
    fname = f"input_{int(time.time())}.wav"
    wav.write(fname, sr, audio)
    return fname

def speech_to_text(wav_path: str) -> str:
    # Usar modelo global carregado
    result = whisper_model.transcribe(wav_path, language="pt")
    return result["text"].strip()

def ask_llm(prompt: str) -> str:
    try:
        from openai import OpenAI
        client = OpenAI(
            api_key=openai.api_key,
            base_url=openai.api_base
        )
        response = client.chat.completions.create(
            model=LLM_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"❌ Erro na API da OpenAI: {e}")
        return "Desculpe, houve um erro ao processar sua pergunta."

########################
# Haupt-Loop
########################
if __name__ == "__main__":
    print("🤖 Assistente de voz local iniciado – Ctrl-C para sair")
    try:
        while True:
            wav_file = record(RECORD_SECS)
            question = speech_to_text(wav_file)
            os.remove(wav_file)
            if not question:
                continue
            print(f"📝 Você disse: {question}")

            answer = ask_llm(question)
            print(f"🤖 Resposta: {answer}")

            say_text(answer)
    except KeyboardInterrupt:
        print("\n👋 Até logo!")


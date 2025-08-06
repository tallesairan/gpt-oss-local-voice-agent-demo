import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import whisper
import ollama
import subprocess, os, time, tempfile
from TTS.api import TTS

########################
# Konfiguration
########################
SAMPLERATE     = 16_000        # Hz
RECORD_SECS    = 4             # Länge einer Aufnahme
LLM_MODEL      = "gpt-oss:20b" # oder kleiner, z. B. gpt-oss:7b
WHISPER_MODEL  = "tiny"        # tiny / base / small / medium …
XTTS_MODEL     = "tts_models/multilingual/multi-dataset/xtts_v2"
XTTS_LANGUAGE  = "de"
SYSTEM_PROMPT  = (
    "Du bist ein hilfreicher Assistent. "
    "Interpretiere Fragen ausschließlich als Deutsch "
    "und antworte immer auf Deutsch. "
    "Nutze keine anderen Sprachen."
)

########################
# TTS initialisieren (einmalig, nicht in der Schleife!)
########################
tts = TTS(model_name=XTTS_MODEL, progress_bar=False, gpu=False)

def say_text(text: str):
    """Erzeugt WAV via XTTS und spielt sie sofort ab (macOS: afplay)."""
    try:
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            tmp_path = tmp.name
        
        tts.tts_to_file(
            text=text,
            language=XTTS_LANGUAGE,
            speaker="Claribel Dervla",  # Standard englischer Speaker
            file_path=tmp_path,
        )
        
        subprocess.run(["afplay", tmp_path])
        os.remove(tmp_path)
        print(f"🔊 TTS: {text}")
        
    except Exception as e:
        print(f"❌ TTS Fehler: {e}")
        # Fallback zu macOS say
        subprocess.run(["say", "-v", "Anna", text])

########################
# STT- & LLM-Funktionen
########################
def record(seconds: int, sr: int = SAMPLERATE) -> str:
    print("🎙️  Sprich jetzt …")
    audio = sd.rec(int(seconds * sr), samplerate=sr, channels=1, dtype='int16')
    sd.wait()
    fname = f"input_{int(time.time())}.wav"
    wav.write(fname, sr, audio)
    return fname

def speech_to_text(wav_path: str) -> str:
    model = whisper.load_model(WHISPER_MODEL)
    result = model.transcribe(wav_path, language="de")
    return result["text"].strip()

def ask_llm(prompt: str) -> str:
    response = ollama.generate(
        model   = LLM_MODEL,
        prompt  = prompt,
        system  = SYSTEM_PROMPT,
        options = {"temperature": 0.7, "num_ctx": 4096}
    )
    return response["response"].strip()

########################
# Haupt-Loop
########################
if __name__ == "__main__":
    print("🤖 Lokaler Sprachassistent gestartet – Strg-C beendet")
    try:
        while True:
            wav_file = record(RECORD_SECS)
            question = speech_to_text(wav_file)
            os.remove(wav_file)
            if not question:
                continue
            print(f"📝 Du sagst: {question}")

            answer = ask_llm(question)
            print(f"🤖 Antwort: {answer}")

            say_text(answer)
    except KeyboardInterrupt:
        print("\n👋 Bis bald!")


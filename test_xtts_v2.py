#!/usr/bin/env python3
"""
Teste do XTTS V2 implementado corretamente
"""

import os
import tempfile
import subprocess
import numpy as np
import scipy.io.wavfile as wav

# Configurar variável de ambiente
os.environ["COQUI_TOS_AGREED"] = "1"

# Importações para XTTS V2
from TTS.tts.configs.xtts_config import XttsConfig
from TTS.tts.models.xtts import Xtts
from TTS.utils.generic_utils import get_user_data_dir
from TTS.utils.manage import ModelManager

def test_xtts_v2():
    """Testa o XTTS V2 implementado corretamente"""
    
    print("🎵 Teste do XTTS V2")
    print("=" * 40)
    
    # Verificar se o arquivo de referência existe
    reference_file = "reference_voice.wav"
    if not os.path.exists(reference_file):
        print("❌ Arquivo de referência não encontrado!")
        print("Execute: python download_reference_voice.py")
        return False
    
    print(f"✅ Arquivo de referência encontrado: {reference_file}")
    
    # Texto de teste
    test_text = "Olá! Esta é uma voz de teste para verificar a qualidade do sistema de síntese de fala. Como você está hoje?"
    
    try:
        # Baixar e carregar modelo XTTS V2
        print("📥 Baixando modelo XTTS V2...")
        model_name = "tts_models/multilingual/multi-dataset/xtts_v2"
        ModelManager().download_model(model_name)
        model_path = os.path.join(get_user_data_dir("tts"), model_name.replace("/", "--"))
        print("✅ Modelo XTTS V2 baixado!")
        
        print("📥 Carregando modelo XTTS V2...")
        config = XttsConfig()
        config.load_json(os.path.join(model_path, "config.json"))
        
        model = Xtts.init_from_config(config)
        model.load_checkpoint(
            config,
            checkpoint_path=os.path.join(model_path, "model.pth"),
            vocab_path=os.path.join(model_path, "vocab.json"),
            eval=True,
            use_deepspeed=False,  # Desabilitar para CPU
        )
        print("✅ Modelo XTTS V2 carregado!")
        
        # Gerar áudio com configurações otimizadas
        print("🎤 Gerando áudio...")
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            tmp_path = tmp.name
        
        # Obter latents de condicionamento do arquivo de referência
        print("🎵 Processando voz de referência...")
        gpt_cond_latent, speaker_embedding = model.get_conditioning_latents(audio_path=reference_file)
        
        # Gerar áudio com streaming
        print("🎤 Gerando áudio...")
        chunks = model.inference_stream(
            test_text,
            "pt",  # Português
            gpt_cond_latent,
            speaker_embedding,
            repetition_penalty=2.5,
            temperature=0.6,
        )
        
        # Combinar chunks em um arquivo
        audio_data = []
        for chunk in chunks:
            chunk_np = chunk.detach().cpu().numpy().squeeze()
            audio_data.append(chunk_np)
        
        # Combinar todos os chunks
        if audio_data:
            combined_audio = np.concatenate(audio_data)
            
            # Salvar como WAV
            wav.write(tmp_path, 24000, combined_audio)
            
            print("✅ Áudio gerado!")
            print("🔊 Reproduzindo...")
            
            # Reproduzir com qualidade máxima
            subprocess.run(["afplay", "-q", "1", tmp_path])
            
            # Limpar
            os.remove(tmp_path)
            
            print("\n🎯 Teste concluído!")
            print("Como foi a qualidade da voz agora?")
            print("\n💡 Se a voz ainda não estiver boa, você pode:")
            print("   1. Gravar sua própria voz de referência")
            print("   2. Baixar outro arquivo de referência")
            print("   3. Ajustar os parâmetros (temperature, repetition_penalty)")
            
            return True
        else:
            print("❌ Nenhum áudio gerado")
            return False
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

if __name__ == "__main__":
    success = test_xtts_v2()
    if success:
        print("\n🎉 XTTS V2 funcionando!")
    else:
        print("\n⚠️ Problemas com XTTS V2") 
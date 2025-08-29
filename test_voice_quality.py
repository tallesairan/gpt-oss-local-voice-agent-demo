#!/usr/bin/env python3
"""
Teste rápido da qualidade da voz TTS
"""

import os
import tempfile
import subprocess
from TTS.api import TTS

# Configurar variável de ambiente
os.environ["COQUI_TOS_AGREED"] = "1"

def test_current_voice():
    """Testa a voz atual configurada"""
    
    print("🎵 Testando Qualidade da Voz Atual")
    print("=" * 40)
    
    # Texto de teste
    test_text = "Olá! Esta é uma voz de teste para verificar a qualidade do sistema de síntese de fala. Como você está hoje?"
    
    try:
        # Carregar TTS com configurações otimizadas
        print("📥 Carregando modelo TTS...")
        tts = TTS(
            model_name="tts_models/multilingual/multi-dataset/xtts_v2",
            progress_bar=False,
            gpu=False,
            use_cuda=False,
            compute_type="float32"
        )
        print("✅ Modelo carregado!")
        
        # Gerar áudio com configurações otimizadas
        print("🎤 Gerando áudio...")
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            tmp_path = tmp.name
        
        tts.tts_to_file(
            text=test_text,
            language="pt",
            speaker="p230",
            file_path=tmp_path,
            speed=0.85,
            temperature=0.7,
            length_penalty=1.0,
            repetition_penalty=2.0,
        )
        
        print("✅ Áudio gerado!")
        print("🔊 Reproduzindo...")
        
        # Reproduzir com qualidade máxima
        subprocess.run(["afplay", "-q", "1", tmp_path])
        
        # Limpar
        os.remove(tmp_path)
        
        print("\n🎯 Teste concluído!")
        print("Como foi a qualidade da voz?")
        
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    test_current_voice() 
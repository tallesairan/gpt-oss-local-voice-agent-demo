#!/usr/bin/env python3
"""
Teste final da voz TTS corrigida
"""

import os
import tempfile
import subprocess
from TTS.api import TTS

# Configurar variável de ambiente
os.environ["COQUI_TOS_AGREED"] = "1"

def test_voice():
    """Testa a voz TTS corrigida"""
    
    print("🎵 Teste Final da Voz TTS")
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
        # Carregar TTS
        print("📥 Carregando modelo TTS...")
        tts = TTS(
            model_name="tts_models/multilingual/multi-dataset/xtts_v2",
            progress_bar=False,
            gpu=False
        )
        print("✅ Modelo carregado!")
        
        # Gerar áudio com configurações otimizadas
        print("🎤 Gerando áudio...")
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            tmp_path = tmp.name
        
        tts.tts_to_file(
            text=test_text,
            language="pt",
            speaker_wav=reference_file,  # Arquivo de áudio de referência
            file_path=tmp_path,
            speed=0.8,
            temperature=0.6,
            repetition_penalty=2.5,
        )
        
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
        print("   3. Ajustar os parâmetros (speed, temperature)")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

if __name__ == "__main__":
    success = test_voice()
    if success:
        print("\n🎉 Voz funcionando!")
    else:
        print("\n⚠️ Problemas com a voz") 
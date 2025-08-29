#!/usr/bin/env python3
"""
Script para configurar o TTS automaticamente
Aceita a licença e baixa o modelo necessário
"""

import os
import sys

def setup_tts():
    """Configura o TTS aceitando a licença automaticamente"""
    
    # Configurar variável de ambiente para aceitar licença
    os.environ["COQUI_TOS_AGREED"] = "1"
    
    print("🔧 Configurando TTS...")
    
    try:
        from TTS.api import TTS
        
        # Modelo que será usado
        model_name = "tts_models/multilingual/multi-dataset/xtts_v2"
        
        print(f"📥 Baixando modelo: {model_name}")
        
        # Inicializar TTS (isso vai baixar o modelo automaticamente)
        tts = TTS(model_name=model_name, progress_bar=True, gpu=False)
        
        print("✅ TTS configurado com sucesso!")
        print("🎯 Modelo baixado e pronto para uso")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao configurar TTS: {e}")
        return False

if __name__ == "__main__":
    success = setup_tts()
    sys.exit(0 if success else 1) 
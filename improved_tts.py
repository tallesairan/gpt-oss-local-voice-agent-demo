#!/usr/bin/env python3
"""
Script para testar diferentes vozes TTS e encontrar a mais natural
"""

import os
import tempfile
import subprocess
from TTS.api import TTS

# Configurar variável de ambiente
os.environ["COQUI_TOS_AGREED"] = "1"

def test_voice(tts, speaker, text, test_name):
    """Testa uma voz específica"""
    print(f"\n🎤 Testando: {test_name}")
    print(f"   Speaker: {speaker}")
    
    try:
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            tmp_path = tmp.name
        
        # Gerar áudio
        tts.tts_to_file(
            text=text,
            language="pt",
            speaker=speaker,
            file_path=tmp_path,
            speed=0.9,
        )
        
        print(f"✅ Áudio gerado: {tmp_path}")
        print("🔊 Reproduzindo... (pressione Enter para continuar)")
        
        # Reproduzir
        subprocess.run(["afplay", "-q", "1", tmp_path])
        
        input()  # Aguardar usuário
        
        # Limpar
        os.remove(tmp_path)
        return True
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def main():
    """Testa diferentes configurações de voz"""
    
    print("🎵 Testador de Voz TTS - Encontrando a Melhor Voz")
    print("=" * 60)
    
    # Texto de teste
    test_text = "Olá! Esta é uma voz de teste para verificar a qualidade do sistema de síntese de fala."
    
    try:
        # Carregar TTS
        print("📥 Carregando modelo TTS...")
        tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2", 
                  progress_bar=False, gpu=False)
        print("✅ Modelo carregado!")
        
        # Lista de speakers para testar
        speakers_to_test = [
            ("p230", "Voz Feminina 1"),
            ("p231", "Voz Feminina 2"), 
            ("p232", "Voz Feminina 3"),
            ("p233", "Voz Masculina 1"),
            ("p234", "Voz Masculina 2"),
            ("p235", "Voz Masculina 3"),
            ("p236", "Voz Feminina 4"),
            ("p237", "Voz Masculina 4"),
            ("p238", "Voz Feminina 5"),
            ("p239", "Voz Masculina 5"),
        ]
        
        print(f"\n🎯 Vamos testar {len(speakers_to_test)} vozes diferentes")
        print("Para cada voz, você ouvirá o áudio e pode avaliar a qualidade")
        print("Pressione Enter após cada teste para continuar")
        
        results = []
        
        for speaker, name in speakers_to_test:
            success = test_voice(tts, speaker, test_text, name)
            if success:
                results.append((speaker, name))
        
        print("\n" + "=" * 60)
        print("📊 Resultados dos Testes")
        print("=" * 60)
        
        for i, (speaker, name) in enumerate(results, 1):
            print(f"{i}. {name} (Speaker: {speaker})")
        
        print(f"\n✅ {len(results)} vozes testadas com sucesso!")
        print("\n💡 Para usar uma voz específica, atualize o voice_assistant.py:")
        print(f"   speaker='{results[0][0]}'  # {results[0][1]}")
        
    except Exception as e:
        print(f"❌ Erro geral: {e}")

if __name__ == "__main__":
    main() 
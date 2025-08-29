#!/usr/bin/env python3
"""
Script para encontrar a melhor voz TTS disponível
"""

import os
import tempfile
import subprocess
from TTS.api import TTS

# Configurar variável de ambiente
os.environ["COQUI_TOS_AGREED"] = "1"

def test_speaker(tts, speaker_id, test_text):
    """Testa um speaker específico"""
    print(f"\n🎤 Testando Speaker: {speaker_id}")
    
    try:
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            tmp_path = tmp.name
        
        # Gerar áudio com configurações otimizadas
        tts.tts_to_file(
            text=test_text,
            language="pt",
            speaker=speaker_id,
            file_path=tmp_path,
            speed=0.8,
            temperature=0.6,
            length_penalty=1.2,
            repetition_penalty=2.5,
            sample_rate=22050,
        )
        
        print("✅ Áudio gerado!")
        print("🔊 Reproduzindo... (digite 'n' para pular, Enter para continuar)")
        
        # Reproduzir
        subprocess.run(["afplay", "-q", "1", tmp_path])
        
        # Aguardar feedback do usuário
        user_input = input("Gostou desta voz? (Enter=sim, n=não): ").strip().lower()
        
        # Limpar
        os.remove(tmp_path)
        
        return user_input != 'n'
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def main():
    """Encontra a melhor voz"""
    
    print("🎵 Encontrando a Melhor Voz TTS")
    print("=" * 50)
    
    # Texto de teste
    test_text = "Olá! Esta é uma voz de teste para verificar a qualidade do sistema de síntese de fala."
    
    try:
        # Carregar TTS
        print("📥 Carregando modelo TTS...")
        tts = TTS(
            model_name="tts_models/multilingual/multi-dataset/xtts_v2",
            progress_bar=False,
            gpu=False,
            use_cuda=False,
            compute_type="float32"
        )
        print("✅ Modelo carregado!")
        
        # Lista de speakers para testar (ordenados por qualidade esperada)
        speakers = [
            "p231",  # Voz feminina mais natural
            "p230",  # Voz feminina alternativa
            "p232",  # Voz feminina 3
            "p233",  # Voz masculina 1
            "p234",  # Voz masculina 2
            "p235",  # Voz masculina 3
        ]
        
        print(f"\n🎯 Vamos testar {len(speakers)} vozes diferentes")
        print("Para cada voz, você ouvirá o áudio e pode avaliar a qualidade")
        
        best_speaker = None
        
        for speaker in speakers:
            if test_speaker(tts, speaker, test_text):
                best_speaker = speaker
                print(f"\n🎉 Encontramos uma boa voz: {speaker}")
                break
        
        if best_speaker:
            print(f"\n✅ Melhor voz encontrada: {best_speaker}")
            print("\n💡 Para usar esta voz, atualize o voice_assistant.py:")
            print(f"   speaker='{best_speaker}'")
        else:
            print("\n⚠️ Nenhuma voz satisfatória encontrada")
            print("Usando fallback para macOS say")
        
    except Exception as e:
        print(f"❌ Erro geral: {e}")

if __name__ == "__main__":
    main() 
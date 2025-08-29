#!/usr/bin/env python3
"""
Script de diagnóstico para identificar problemas no sistema
"""

import sys
import os
import subprocess
import warnings

def test_imports():
    """Testa se todas as dependências estão funcionando"""
    print("🔍 Testando imports...")
    
    try:
        import sounddevice as sd
        print("✅ sounddevice - OK")
    except Exception as e:
        print(f"❌ sounddevice - Erro: {e}")
        return False
    
    try:
        import numpy as np
        print("✅ numpy - OK")
    except Exception as e:
        print(f"❌ numpy - Erro: {e}")
        return False
    
    try:
        import scipy.io.wavfile as wav
        print("✅ scipy - OK")
    except Exception as e:
        print(f"❌ scipy - Erro: {e}")
        return False
    
    try:
        import whisper
        print("✅ whisper - OK")
    except Exception as e:
        print(f"❌ whisper - Erro: {e}")
        return False
    
    try:
        import openai
        print("✅ openai - OK")
    except Exception as e:
        print(f"❌ openai - Erro: {e}")
        return False
    
    try:
        from TTS.api import TTS
        print("✅ TTS - OK")
    except Exception as e:
        print(f"❌ TTS - Erro: {e}")
        return False
    
    return True

def test_audio():
    """Testa se o sistema de áudio está funcionando"""
    print("\n🎵 Testando sistema de áudio...")
    
    try:
        import sounddevice as sd
        devices = sd.query_devices()
        print(f"✅ Dispositivos de áudio encontrados: {len(devices)}")
        
        # Testar gravação
        print("🎙️ Testando gravação...")
        duration = 1  # 1 segundo
        sample_rate = 16000
        
        recording = sd.rec(int(duration * sample_rate), 
                          samplerate=sample_rate, 
                          channels=1, 
                          dtype='int16')
        sd.wait()
        
        print("✅ Gravação funcionando")
        return True
        
    except Exception as e:
        print(f"❌ Erro no sistema de áudio: {e}")
        return False

def test_whisper():
    """Testa se o Whisper está funcionando"""
    print("\n🤖 Testando Whisper...")
    
    try:
        import whisper
        
        # Suprimir warnings
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            
            print("📥 Carregando modelo...")
            model = whisper.load_model("tiny")
            print("✅ Modelo carregado")
            
            # Criar arquivo de teste
            import numpy as np
            import scipy.io.wavfile as wav
            
            # Gerar áudio de teste (silêncio)
            sample_rate = 16000
            duration = 2
            audio = np.zeros(sample_rate * duration, dtype=np.int16)
            
            test_file = "test_audio.wav"
            wav.write(test_file, sample_rate, audio)
            
            print("🎵 Transcrevendo áudio de teste...")
            result = model.transcribe(test_file, language="pt")
            print(f"✅ Transcrição: '{result['text']}'")
            
            # Limpar arquivo de teste
            os.remove(test_file)
            
        return True
        
    except Exception as e:
        print(f"❌ Erro no Whisper: {e}")
        return False

def test_openai():
    """Testa se a API da OpenAI está funcionando"""
    print("\n🌐 Testando servidor personalizado...")
    
    try:
        import openai
        from openai import OpenAI
        
        # Configurar
        openai.api_base = "https://gpt-proxy.ahvideoscdn.net/v1"
        openai.api_key = "dummy-key"
        
        client = OpenAI(
            api_key=openai.api_key,
            base_url=openai.api_base
        )
        
        print("💬 Testando chat...")
        response = client.chat.completions.create(
            model="gpt-oss-1",
            messages=[
                {"role": "user", "content": "Teste"}
            ],
            max_tokens=10
        )
        
        print(f"✅ Resposta recebida: {response.choices[0].message.content}")
        return True
        
    except Exception as e:
        print(f"❌ Erro na API: {e}")
        return False

def test_tts():
    """Testa se o TTS está funcionando"""
    print("\n🔊 Testando TTS...")
    
    try:
        # Configurar variável de ambiente
        os.environ["COQUI_TOS_AGREED"] = "1"
        
        from TTS.api import TTS
        
        print("📥 Carregando modelo TTS...")
        tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2", 
                  progress_bar=False, gpu=False)
        print("✅ Modelo TTS carregado")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro no TTS: {e}")
        return False

def main():
    """Executa todos os testes de diagnóstico"""
    print("🔧 Diagnóstico do Sistema de Assistente de Voz")
    print("=" * 50)
    
    tests = [
        ("Imports", test_imports),
        ("Áudio", test_audio),
        ("Whisper", test_whisper),
        ("OpenAI", test_openai),
        ("TTS", test_tts)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Erro inesperado em {test_name}: {e}")
            results.append((test_name, False))
    
    print("\n" + "=" * 50)
    print("📊 Resultados do Diagnóstico:")
    
    all_passed = True
    for test_name, result in results:
        status = "✅ PASSOU" if result else "❌ FALHOU"
        print(f"  {test_name}: {status}")
        if not result:
            all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 Todos os testes passaram! Sistema funcionando corretamente.")
    else:
        print("⚠️ Alguns testes falharam. Verifique os erros acima.")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 
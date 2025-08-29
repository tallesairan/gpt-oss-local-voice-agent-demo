#!/usr/bin/env python3
"""
Script para baixar um arquivo de voz de referência de qualidade para XTTS
"""

import os
import requests
import subprocess

def download_reference_voice():
    """Baixa um arquivo de voz de referência de qualidade"""
    
    print("🎵 Baixando arquivo de voz de referência...")
    
    # URL de um arquivo de voz de referência de qualidade
    # Vamos usar um exemplo do Coqui TTS
    voice_url = "https://huggingface.co/coqui/XTTS-v2/resolve/main/samples/female.wav"
    
    reference_file = "reference_voice.wav"
    
    try:
        print(f"📥 Baixando de: {voice_url}")
        
        # Baixar o arquivo
        response = requests.get(voice_url, stream=True)
        response.raise_for_status()
        
        with open(reference_file, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print(f"✅ Arquivo baixado: {reference_file}")
        
        # Verificar se o arquivo é válido
        if os.path.exists(reference_file) and os.path.getsize(reference_file) > 0:
            print("✅ Arquivo de referência válido!")
            return True
        else:
            print("❌ Arquivo inválido")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao baixar: {e}")
        return False

def create_simple_reference():
    """Cria um arquivo de referência simples usando macOS say"""
    
    print("🎤 Criando arquivo de referência simples...")
    
    reference_file = "reference_voice.wav"
    
    try:
        # Usar macOS say para criar um arquivo de referência
        subprocess.run([
            "say", 
            "-v", "Victoria",  # Voz feminina de qualidade
            "-o", reference_file,
            "Olá, esta é minha voz de referência para o sistema de síntese de fala."
        ], check=True)
        
        if os.path.exists(reference_file) and os.path.getsize(reference_file) > 0:
            print(f"✅ Arquivo de referência criado: {reference_file}")
            return True
        else:
            print("❌ Falha ao criar arquivo")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao criar arquivo: {e}")
        return False

def main():
    """Função principal"""
    
    print("🎵 Configurando Voz de Referência para XTTS")
    print("=" * 50)
    
    reference_file = "reference_voice.wav"
    
    # Verificar se já existe
    if os.path.exists(reference_file):
        print(f"✅ Arquivo de referência já existe: {reference_file}")
        return True
    
    # Tentar baixar primeiro
    if download_reference_voice():
        return True
    
    # Se falhar, criar um simples
    print("\n🔄 Tentando criar arquivo de referência simples...")
    if create_simple_reference():
        return True
    
    print("\n❌ Não foi possível criar arquivo de referência")
    print("💡 Você pode:")
    print("   1. Gravar um arquivo de áudio manualmente")
    print("   2. Usar o fallback do macOS say")
    print("   3. Baixar um arquivo de voz de qualidade")
    
    return False

if __name__ == "__main__":
    success = main()
    if success:
        print("\n🎉 Configuração concluída!")
    else:
        print("\n⚠️ Configuração incompleta") 
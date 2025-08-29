#!/usr/bin/env python3
"""
Script para testar a conectividade com o servidor personalizado
"""

import openai
import sys

def test_server():
    """Testa a conectividade com o servidor personalizado"""
    
    # Configurar o servidor personalizado
    openai.api_base = "https://gpt-proxy.ahvideoscdn.net/v1"
    openai.api_key = "dummy-key"
    
    print("🔍 Testando servidor personalizado...")
    print(f"📍 Endpoint: {openai.api_base}")
    
    try:
        from openai import OpenAI
        
        client = OpenAI(
            api_key=openai.api_key,
            base_url=openai.api_base
        )
        
        # Teste 1: Listar modelos
        print("\n📋 Testando listagem de modelos...")
        models = client.models.list()
        print(f"✅ Modelos disponíveis: {len(models.data)}")
        for model in models.data:
            print(f"   - {model.id}")
        
        # Teste 2: Testar chat
        print("\n💬 Testando chat...")
        response = client.chat.completions.create(
            model="gpt-oss-1",
            messages=[
                {"role": "user", "content": "Olá, como você está?"}
            ],
            max_tokens=50
        )
        
        print(f"✅ Resposta recebida: {response.choices[0].message.content}")
        
        print("\n🎉 Todos os testes passaram! Servidor funcionando corretamente.")
        return True
        
    except Exception as e:
        print(f"\n❌ Erro ao testar servidor: {e}")
        print("\n🔧 Possíveis soluções:")
        print("   1. Verifique se o servidor está rodando")
        print("   2. Confirme se o endpoint está correto")
        print("   3. Teste a conectividade: curl https://gpt-proxy.ahvideoscdn.net/v1/models")
        return False

if __name__ == "__main__":
    success = test_server()
    sys.exit(0 if success else 1) 
# 🔧 Configuração do Servidor Personalizado

Este projeto está configurado para usar um servidor personalizado que imita a API da OpenAI.

## 📋 Configuração Atual

### Endpoint do Servidor
```
https://gpt-proxy.ahvideoscdn.net/v1
```

### Modelo Utilizado
```
gpt-oss-1
```

### Configuração no Código
```python
# voice_assistant.py
openai.api_base = "https://gpt-proxy.ahvideoscdn.net/v1"
openai.api_key = "dummy-key"  # Chave dummy já que o servidor é seu
LLM_MODEL = "gpt-oss-1"
```

## 🚀 Como Funciona

O servidor personalizado implementa a mesma interface da API da OpenAI, incluindo:

- **`/chat/completions`** - Para geração de texto
- **`/models`** - Para listar modelos disponíveis
- **`/embeddings`** - Para embeddings (se necessário)

### Exemplo de Requisição
```python
response = openai.ChatCompletion.create(
    model="gpt-oss-1",
    messages=[
        {"role": "system", "content": "Você é um assistente útil."},
        {"role": "user", "content": "Olá, como você está?"}
    ],
    temperature=0.7,
    max_tokens=1000
)
```

## ✅ Vantagens

- ✅ **Sem custos de API** - O servidor é seu
- ✅ **Controle total** - Você gerencia o servidor
- ✅ **Compatibilidade** - Usa a mesma interface da OpenAI
- ✅ **Privacidade** - Dados não saem da sua infraestrutura

## 🔧 Personalização

### Mudar Endpoint
```python
openai.api_base = "https://seu-novo-endpoint.com/v1"
```

### Mudar Modelo
```python
LLM_MODEL = "seu-modelo-personalizado"
```

### Adicionar Headers Customizados
```python
import openai
openai.api_base = "https://gpt-proxy.ahvideoscdn.net/v1"
openai.api_key = "dummy-key"

# Para adicionar headers customizados (se necessário)
import requests
openai.api_requestor._session.headers.update({
    "X-Custom-Header": "valor"
})
```

## 🆘 Solução de Problemas

### Erro: "Connection refused"
- Verifique se o servidor está rodando
- Confirme se o endpoint está correto
- Teste a conectividade: `curl https://gpt-proxy.ahvideoscdn.net/v1/models`

### Erro: "Model not found"
- Verifique se o modelo `gpt-oss-1` está disponível no servidor
- Liste os modelos: `curl https://gpt-proxy.ahvideoscdn.net/v1/models`

### Erro: "Rate limit exceeded"
- Aguarde alguns segundos entre requisições
- Verifique os limites do seu servidor

## 📞 Suporte

Para problemas relacionados ao servidor:
1. Verifique os logs do servidor
2. Teste o endpoint diretamente com curl
3. Confirme se o modelo está disponível 
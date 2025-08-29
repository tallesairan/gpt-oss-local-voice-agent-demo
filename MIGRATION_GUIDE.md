# 🔄 Guia de Migração: Ollama → Servidor OpenAI Personalizado

Este guia explica as mudanças feitas para migrar do Ollama para um servidor personalizado que imita a API da OpenAI.

## 📋 Mudanças Principais

### 1. Dependências
- **Removido**: `ollama>=0.1.7`
- **Adicionado**: `openai>=1.0.0`

### 2. Configuração
- **Modelo**: Mudou de `gpt-oss:20b` para `gpt-oss-1`
- **Idioma**: Mudou de alemão (`de`) para português (`pt`)
- **Servidor**: Agora usa servidor personalizado em `https://gpt-proxy.ahvideoscdn.net/v1`

### 3. Função `ask_llm()`
**Antes (Ollama):**
```python
def ask_llm(prompt: str) -> str:
    response = ollama.generate(
        model   = LLM_MODEL,
        prompt  = prompt,
        system  = SYSTEM_PROMPT,
        options = {"temperature": 0.7, "num_ctx": 4096}
    )
    return response["response"].strip()
```

**Depois (Servidor Personalizado):**
```python
def ask_llm(prompt: str) -> str:
    try:
        response = openai.ChatCompletion.create(
            model=LLM_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"❌ Erro no servidor personalizado: {e}")
        return "Desculpe, houve um erro ao processar sua pergunta."
```

## 🚀 Como Configurar

### 1. Servidor Personalizado
O servidor já está configurado e funcionando em:
```
https://gpt-proxy.ahvideoscdn.net/v1
```

### 2. Configurar o Projeto
```bash
# Instalar dependências atualizadas
pip install -r requirements.txt

# Configuração já está pronta no código
```

### 3. Testar
```bash
python voice_assistant.py
```

## ⚠️ Considerações Importantes

### Vantagens do Servidor Personalizado:
- ✅ Respostas rápidas e consistentes
- ✅ Controle total sobre o servidor
- ✅ Sem custos de API
- ✅ Dados não saem da sua infraestrutura
- ✅ Melhor suporte para português

### Desvantagens:
- ❌ Requer conexão com internet
- ❌ Dependência do seu servidor estar online
- ❌ Necessidade de manutenção do servidor

### Custos:
- **$0** - O servidor é seu, sem custos de API

## 🔧 Personalização

### Mudar Modelo
```python
LLM_MODEL = "seu-modelo-personalizado"  # Para usar outro modelo
```

### Ajustar Parâmetros
```python
response = openai.ChatCompletion.create(
    model=LLM_MODEL,
    messages=[...],
    temperature=0.5,    # Menos criativo
    max_tokens=500,     # Respostas mais curtas
    top_p=0.9,          # Controle de diversidade
)
```

### Usar Outros Idiomas
```python
XTTS_LANGUAGE = "en"  # Inglês
# ou
XTTS_LANGUAGE = "es"  # Espanhol
```

## 🆘 Solução de Problemas

### Erro: "Connection refused"
- Verifique se o servidor está rodando
- Confirme se o endpoint está correto
- Teste: `curl https://gpt-proxy.ahvideoscdn.net/v1/models`

### Erro: "Model not found"
- Verifique se o modelo `gpt-oss-1` está disponível no servidor
- Liste os modelos: `curl https://gpt-proxy.ahvideoscdn.net/v1/models`

### Erro: "Rate limit exceeded"
- Aguarde alguns segundos entre requisições
- Verifique os limites do seu servidor

## 📞 Suporte

Se encontrar problemas:
1. Verifique os logs de erro
2. Teste o endpoint diretamente com curl
3. Verifique se o servidor está funcionando corretamente 
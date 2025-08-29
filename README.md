# 🎙️ GPT-OSS Local Voice Agent Demo

> Modern local voice assistant with React frontend and Python backend using custom OpenAI-compatible server, Whisper, and XTTS

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Node.js 16+](https://img.shields.io/badge/node-16+-green.svg)](https://nodejs.org/)
[![YouTube](https://img.shields.io/badge/YouTube-@everlastai-red?logo=youtube)](https://www.youtube.com/@everlastai)

**📺 [Watch the tutorial](https://www.youtube.com/@everlastai) • 💬 [Get free consultation](https://kiberatung.de) • 📞 [AI phone solutions](https://kitelefonagent.de)**

**Live Demo Features:** Chat Interface • Voice Mode • Real-time Processing • Modern UI • Completely Local

---

## ✨ Features

- 💬 **Chat Interface**: Text conversation with local AI models
- 🎤 **Voice Mode**: Speech-to-text with natural voice responses  
- 🔄 **Real-time Status**: Live feedback during processing
- 🎨 **Modern UI**: Beautiful React interface with smooth animations
- 🌐 **Hybrid Local/Custom**: Local audio processing with custom OpenAI-compatible server for LLM
- 🔧 **Open Source**: Extend and customize as needed

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+** (3.11+ recommended)
- **Node.js 16+** 
- **Custom OpenAI-compatible server** (already configured)

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/everlastconsulting/gpt-oss-local-voice-agent-demo.git
cd gpt-oss-local-voice-agent-demo

# 2. Backend setup
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# 3. Frontend setup
npm install

# 4. Configuration is already set up
# Using custom server: https://gpt-proxy.ahvideoscdn.net/v1
# Model: gpt-oss-1

# 5. Test the server (optional)
python test_server.py

# 6. Start the application
./start.sh  # Starts both backend and frontend
```

**Access the app at: http://localhost:3000**

## 🎯 Usage

### Chat Mode
1. Type your message and press Enter
2. Get AI responses in real-time

### Voice Mode  
1. Click "Voice Mode" button
2. Click microphone and speak your question
3. Watch real-time transcription
4. Listen to AI voice response

## ⚙️ Configuration

Configuration is already set up:

```python
# Custom OpenAI-compatible server
openai.api_base = "https://gpt-proxy.ahvideoscdn.net/v1"
openai.api_key = "dummy-key"
LLM_MODEL = "gpt-oss-1"

# Audio Settings
RECORD_DURATION=4
TTS_LANGUAGE=pt

# Server
FLASK_RUN_PORT=8080
```

## 🛠️ Tech Stack

- **Frontend**: React, Tailwind CSS, Framer Motion
- **Backend**: Flask, Python
- **AI/ML**: Custom OpenAI-compatible server (LLM), Whisper (STT), XTTS (TTS)
- **Audio**: SoundDevice, NumPy, SciPy

## 🔧 Troubleshooting

### TTS License Issue
Se você encontrar um erro de licença do TTS:
```bash
# Execute o script de setup
python setup_tts.py
```

### Server Connection Issue
Para testar a conectividade com o servidor:
```bash
# Teste o servidor
python test_server.py

# Ou teste manualmente
curl https://gpt-proxy.ahvideoscdn.net/v1/models
```

### Frontend Warnings
Os warnings do ESLint foram corrigidos. Se ainda aparecerem:
```bash
# No diretório do projeto
npm run build
```

### Melhorar Qualidade da Voz
Para configurar e testar a voz TTS:
```bash
# Baixar arquivo de referência de voz
python download_reference_voice.py

# Testar voz atual
python test_voice_final.py

# Testar assistente completo
python voice_assistant.py
```

### Configurações de Voz Otimizadas
O sistema está configurado com:
- **Arquivo de referência**: reference_voice.wav (voz feminina de qualidade)
- **Velocidade**: 0.8 (mais lenta para naturalidade)
- **Temperatura**: 0.6 (menos variação)
- **Repetition penalty**: 2.5 (evitar repetições)
- **Qualidade de áudio**: Máxima

## 🤝 Contributing

This is a **demo project** - feel free to:

- 🌟 **Star** if you find it useful
- 🐛 **Report issues** you encounter  
- 💡 **Suggest features** in discussions
- 🔧 **Submit pull requests** for improvements

### Quick Ideas
- 🌍 Add more languages
- 🎨 Improve UI/UX
- 📱 Mobile responsiveness
- ⚡ Performance optimizations

## 🎥 Learn More

This project was created as part of our AI development series. Check out:

- 📺 **YouTube Channel**: [EverLast AI](https://www.youtube.com/@everlastai) - AI tutorials and demos
- 💬 **Free Consultation**: [kiberatung.de](https://kiberatung.de) - Get expert AI advice
- 📞 **AI Phone Assistants**: [kitelefonagent.de](https://kitelefonagent.de) - Professional AI phone solutions

## 📝 License

MIT License - see [LICENSE](LICENSE) file

## 🙏 Acknowledgments

- Custom OpenAI-compatible server for LLM functionality
- [OpenAI Whisper](https://openai.com/research/whisper) for speech recognition
- [Coqui TTS](https://github.com/coqui-ai/TTS) for text-to-speech

---

⭐ **Star this repo if you like it!** ⭐

**Built with ❤️ for the open source community**

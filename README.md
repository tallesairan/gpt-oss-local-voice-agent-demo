# 🎙️ GPT-OSS Local Voice Agent Demo

> Modern local voice assistant with React frontend and Python backend using Ollama, Whisper, and XTTS

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Node.js 16+](https://img.shields.io/badge/node-16+-green.svg)](https://nodejs.org/)

**Live Demo Features:** Chat Interface • Voice Mode • Real-time Processing • Modern UI • Completely Local

---

## ✨ Features

- 💬 **Chat Interface**: Text conversation with local AI models
- 🎤 **Voice Mode**: Speech-to-text with natural voice responses  
- 🔄 **Real-time Status**: Live feedback during processing
- 🎨 **Modern UI**: Beautiful React interface with smooth animations
- 🌐 **Completely Local**: No cloud services, full privacy
- 🔧 **Open Source**: Extend and customize as needed

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+** (3.11+ recommended)
- **Node.js 16+** 
- **Ollama** ([Install here](https://ollama.ai))

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

# 4. Configure Ollama
ollama pull llama2  # or gpt-oss:20b for German

# 5. Start the application
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

Create `.env` file for custom settings:

```env
# Ollama Model
OLLAMA_MODEL=gpt-oss:20b

# Audio Settings
RECORD_DURATION=4
TTS_LANGUAGE=de

# Server
FLASK_RUN_PORT=8080
```

## 🛠️ Tech Stack

- **Frontend**: React, Tailwind CSS, Framer Motion
- **Backend**: Flask, Python
- **AI/ML**: Ollama (LLM), Whisper (STT), XTTS (TTS)
- **Audio**: SoundDevice, NumPy, SciPy

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

## 📝 License

MIT License - see [LICENSE](LICENSE) file

## 🙏 Acknowledgments

- [Ollama](https://ollama.ai) for local LLM hosting
- [OpenAI Whisper](https://openai.com/research/whisper) for speech recognition
- [Coqui TTS](https://github.com/coqui-ai/TTS) for text-to-speech

---

⭐ **Star this repo if you like it!** ⭐

**Built with ❤️ for the open source community**

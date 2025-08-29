#!/bin/bash

# Voice Assistant Startup Script
echo "🎙️ Starting Local Voice Assistant..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Install Python dependencies
echo "📥 Installing Python dependencies..."
pip install -r requirements.txt

# Setup TTS (accept license and download model)
echo "🔧 Setting up TTS..."
python setup_tts.py

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📦 Installing Node.js dependencies..."
    npm install
fi

# Check if custom server is accessible
echo "🔍 Checking custom OpenAI server..."
echo "✅ Using custom server: https://gpt-proxy.ahvideoscdn.net/v1"

# Start backend server in background
echo "🚀 Starting backend server..."
python backend_server.py &
BACKEND_PID=$!

# Wait a moment for backend to start
sleep 3

# Start frontend
echo "🌐 Starting React frontend..."
npm start &
FRONTEND_PID=$!

# Function to handle cleanup
cleanup() {
    echo "🛑 Shutting down servers..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    exit 0
}

# Handle Ctrl+C
trap cleanup SIGINT

echo "✅ Voice Assistant is starting up!"
echo "🌐 Frontend: http://localhost:3000"
echo "🔌 Backend: http://localhost:5000"
echo "📋 Health Check: http://localhost:5000/health"
echo ""
echo "Press Ctrl+C to stop all servers"

# Wait for user to stop
wait
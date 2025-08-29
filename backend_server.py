from flask import Flask, request, jsonify
from flask_cors import CORS
import threading
import time
import os
import tempfile
from voice_assistant import (
    record, speech_to_text, ask_llm, say_text,
    RECORD_SECS, LLM_MODEL, WHISPER_MODEL, SYSTEM_PROMPT
)

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Global state for voice recording
recording_state = {
    'is_recording': False,
    'is_processing': False,
    'is_speaking': False,
    'last_transcription': '',
    'last_response': '',
    'audio_file': None,
    'error': None
}

# Thread lock for state management
state_lock = threading.Lock()

def update_state(**kwargs):
    """Thread-safe state updates"""
    with state_lock:
        recording_state.update(kwargs)

def get_state():
    """Thread-safe state reading"""
    with state_lock:
        return recording_state.copy()

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'Voice Assistant Backend is running',
        'model': LLM_MODEL,
        'whisper': WHISPER_MODEL
    })

@app.route('/config', methods=['GET'])
def get_config():
    """Get current configuration"""
    return jsonify({
        'llm_model': LLM_MODEL,
        'whisper_model': WHISPER_MODEL,
        'record_seconds': RECORD_SECS,
        'system_prompt': SYSTEM_PROMPT
    })

@app.route('/chat', methods=['POST'])
def chat():
    """Handle text chat messages"""
    try:
        data = request.get_json()
        message = data.get('message', '').strip()
        
        if not message:
            return jsonify({'error': 'Nenhuma mensagem recebida'}), 400
        
        # Get response from LLM
        response = ask_llm(message)
        
        return jsonify({
            'message': message,
            'response': response,
            'timestamp': time.time()
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/voice/start', methods=['POST'])
def start_voice_recording():
    """Start voice recording"""
    try:
        state = get_state()
        
        if state['is_recording'] or state['is_processing']:
            return jsonify({'error': 'Gravação já ativa'}), 400
        
        update_state(
            is_recording=True,
            is_processing=False,
            is_speaking=False,
            last_transcription='',
            last_response='',
            error=None
        )
        
        def record_audio():
            try:
                # Record audio
                audio_file = record(RECORD_SECS)
                update_state(audio_file=audio_file)
                
            except Exception as e:
                update_state(
                    is_recording=False,
                    error=str(e)
                )
        
        # Start recording in background
        threading.Thread(target=record_audio, daemon=True).start()
        
        return jsonify({
            'message': 'Gravação iniciada',
            'duration': RECORD_SECS
        })
        
    except Exception as e:
        update_state(is_recording=False, error=str(e))
        return jsonify({'error': str(e)}), 500

@app.route('/voice/stop', methods=['POST'])
def stop_voice_recording():
    """Stop voice recording and process"""
    try:
        state = get_state()
        
        if not state['is_recording'] and not state['audio_file']:
            return jsonify({'error': 'Nenhuma gravação ativa'}), 400
        
        update_state(
            is_recording=False,
            is_processing=True
        )
        
        def process_audio():
            try:
                state = get_state()
                audio_file = state['audio_file']
                
                if not audio_file or not os.path.exists(audio_file):
                    update_state(
                        is_processing=False,
                        error='Arquivo de áudio não encontrado'
                    )
                    return
                
                # Speech to text
                transcription = speech_to_text(audio_file)
                update_state(last_transcription=transcription)
                
                # Clean up audio file
                try:
                    os.remove(audio_file)
                except:
                    pass
                
                if not transcription.strip():
                    update_state(
                        is_processing=False,
                        error='Nenhuma fala detectada'
                    )
                    return
                
                # Get LLM response
                response = ask_llm(transcription)
                update_state(last_response=response)
                
                # Speak response
                update_state(
                    is_processing=False,
                    is_speaking=True
                )
                
                say_text(response)
                
                update_state(is_speaking=False)
                
            except Exception as e:
                update_state(
                    is_recording=False,
                    is_processing=False,
                    is_speaking=False,
                    error=str(e)
                )
        
        # Process in background
        threading.Thread(target=process_audio, daemon=True).start()
        
        return jsonify({
            'message': 'Processamento iniciado'
        })
        
    except Exception as e:
        update_state(
            is_recording=False,
            is_processing=False,
            error=str(e)
        )
        return jsonify({'error': str(e)}), 500

@app.route('/voice/status', methods=['GET'])
def get_voice_status():
    """Get current voice recording status"""
    state = get_state()
    return jsonify({
        'recording': state['is_recording'],
        'processing': state['is_processing'],
        'speaking': state['is_speaking'],
        'lastTranscription': state['last_transcription'],
        'lastResponse': state['last_response'],
        'error': state['error'],
        'timestamp': time.time()
    })

@app.route('/voice/cancel', methods=['POST'])
def cancel_voice_operation():
    """Cancel current voice operation"""
    try:
        state = get_state()
        
        # Clean up audio file if exists
        if state['audio_file'] and os.path.exists(state['audio_file']):
            try:
                os.remove(state['audio_file'])
            except:
                pass
        
        update_state(
            is_recording=False,
            is_processing=False,
            is_speaking=False,
            audio_file=None,
            error=None
        )
        
        return jsonify({'message': 'Operação cancelada'})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    port = int(os.getenv("FLASK_RUN_PORT", 8080))
    print("🚀 Starting Voice Assistant Backend Server...")
    print("🌐 Frontend: http://localhost:3000")
    print(f"🔌 Backend API:  http://localhost:{port}")
    print(f"📋 Health Check: http://localhost:{port}/health")
    print("\n💡 To start the React frontend, run:")
    print("   npm start")
    print("\n✅ Usando servidor personalizado: https://gpt-proxy.ahvideoscdn.net/v1")
    
    app.run(host="0.0.0.0", port=port, debug=True)
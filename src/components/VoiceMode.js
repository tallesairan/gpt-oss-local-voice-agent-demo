import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Mic, MicOff, Volume2, Settings } from 'lucide-react';
import { startRecording, stopRecording, getCurrentStatus } from '../services/api';

const VoiceMode = ({ isConnected }) => {
  const [isRecording, setIsRecording] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [currentText, setCurrentText] = useState('');
  const [lastResponse, setLastResponse] = useState('');
  const [recordingDuration, setRecordingDuration] = useState(0);
  // Removido isListening pois não está sendo usado
  
  const intervalRef = useRef(null);
  const statusIntervalRef = useRef(null);

  useEffect(() => {
    // Check status every second
    if (isConnected) {
      statusIntervalRef.current = setInterval(checkStatus, 1000);
    }
    
    return () => {
      if (intervalRef.current) clearInterval(intervalRef.current);
      if (statusIntervalRef.current) clearInterval(statusIntervalRef.current);
    };
  }, [isConnected]);

  const checkStatus = async () => {
    try {
      const status = await getCurrentStatus();
      setIsProcessing(status.processing);
      setIsSpeaking(status.speaking);
      if (status.lastResponse) {
        setLastResponse(status.lastResponse);
      }
    } catch (error) {
      console.error('Status check failed:', error);
    }
  };

  const handleVoiceToggle = async () => {
    if (!isConnected) return;

    if (isRecording) {
      // Stop recording
      setIsRecording(false);
      setIsProcessing(true);
      clearInterval(intervalRef.current);
      
      try {
        const response = await stopRecording();
        setCurrentText(response.transcription);
        setLastResponse(response.response);
      } catch (error) {
        console.error('Recording failed:', error);
        setCurrentText('Fehler bei der Aufnahme');
      } finally {
        setIsProcessing(false);
        setRecordingDuration(0);
      }
    } else {
      // Start recording
      setIsRecording(true);
      setCurrentText('');
      setRecordingDuration(0);
      
      // Start timer
      intervalRef.current = setInterval(() => {
        setRecordingDuration(prev => prev + 1);
      }, 1000);
      
      try {
        await startRecording();
      } catch (error) {
        console.error('Failed to start recording:', error);
        setIsRecording(false);
        clearInterval(intervalRef.current);
      }
    }
  };

  const formatDuration = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  const VoiceWaveform = () => (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="flex items-center justify-center space-x-1 h-16"
    >
      {[...Array(10)].map((_, i) => (
        <motion.div
          key={i}
          className={`voice-wave ${
            isSpeaking || isRecording ? 'h-8' : 'h-2'
          }`}
          animate={{
            height: isSpeaking || isRecording 
              ? [8, 32, 16, 40, 24, 32, 12, 36, 20, 32][i] 
              : 8
          }}
          transition={{
            duration: 0.5,
            repeat: isSpeaking || isRecording ? Infinity : 0,
            repeatType: 'mirror',
            delay: i * 0.1
          }}
        />
      ))}
    </motion.div>
  );

  const StatusIndicator = () => (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      className="text-center space-y-2"
    >
      {isRecording && (
        <div className="text-lg font-medium text-red-600">
          🎙️ Aufnahme läuft... {formatDuration(recordingDuration)}
        </div>
      )}
      
      {isProcessing && (
        <div className="text-lg font-medium text-blue-600">
          🤔 Verarbeite deine Anfrage...
        </div>
      )}
      
      {isSpeaking && (
        <div className="text-lg font-medium text-green-600">
          🔊 Assistant spricht...
        </div>
      )}
      
      {!isRecording && !isProcessing && !isSpeaking && (
        <div className="text-lg font-medium text-gray-600">
          👂 Bereit zum Zuhören
        </div>
      )}
    </motion.div>
  );

  return (
    <div className="max-w-4xl mx-auto">
      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        className="bg-white rounded-3xl shadow-2xl border border-gray-200 overflow-hidden"
      >
        {/* Voice Mode Header */}
        <div className="bg-gradient-to-r from-purple-500 to-indigo-600 p-8 text-white text-center">
          <motion.div
            initial={{ y: -20 }}
            animate={{ y: 0 }}
            className="space-y-2"
          >
            <h2 className="text-2xl font-bold">Voice Mode</h2>
            <p className="text-purple-100">
              Sprich mit deinem lokalen Assistant
            </p>
          </motion.div>
        </div>

        {/* Main Voice Interface */}
        <div className="p-12">
          <div className="text-center space-y-8">
            {/* Voice Button */}
            <motion.div
              className="relative flex justify-center"
              whileHover={{ scale: 1.02 }}
            >
              {/* Pulse rings for active state */}
              <AnimatePresence>
                {(isRecording || isSpeaking) && (
                  <>
                    <motion.div
                      initial={{ scale: 0.8, opacity: 1 }}
                      animate={{ scale: 2, opacity: 0 }}
                      exit={{ scale: 0.8, opacity: 1 }}
                      transition={{ duration: 2, repeat: Infinity }}
                      className="absolute w-24 h-24 border-2 border-primary-300 rounded-full"
                    />
                    <motion.div
                      initial={{ scale: 0.8, opacity: 1 }}
                      animate={{ scale: 1.5, opacity: 0 }}
                      exit={{ scale: 0.8, opacity: 1 }}
                      transition={{ duration: 2, repeat: Infinity, delay: 0.5 }}
                      className="absolute w-24 h-24 border-2 border-primary-400 rounded-full"
                    />
                  </>
                )}
              </AnimatePresence>

              <motion.button
                onClick={handleVoiceToggle}
                disabled={!isConnected || isProcessing}
                whileTap={{ scale: 0.95 }}
                className={`relative w-24 h-24 rounded-full flex items-center justify-center text-white text-2xl font-semibold shadow-2xl transition-all duration-300 ${
                  isRecording
                    ? 'bg-red-500 hover:bg-red-600'
                    : isProcessing
                    ? 'bg-blue-500'
                    : isSpeaking
                    ? 'bg-green-500'
                    : isConnected
                    ? 'bg-primary-500 hover:bg-primary-600'
                    : 'bg-gray-400 cursor-not-allowed'
                }`}
              >
                {isProcessing ? (
                  <motion.div
                    animate={{ rotate: 360 }}
                    transition={{ duration: 1, repeat: Infinity, ease: 'linear' }}
                  >
                    <Settings className="w-8 h-8" />
                  </motion.div>
                ) : isSpeaking ? (
                  <Volume2 className="w-8 h-8" />
                ) : isRecording ? (
                  <MicOff className="w-8 h-8" />
                ) : (
                  <Mic className="w-8 h-8" />
                )}
              </motion.button>
            </motion.div>

            {/* Status */}
            <StatusIndicator />

            {/* Waveform Visualization */}
            {(isRecording || isSpeaking) && <VoiceWaveform />}

            {/* Current Text Display */}
            <AnimatePresence>
              {currentText && (
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -20 }}
                  className="bg-gray-50 border border-gray-200 rounded-2xl p-6 max-w-2xl mx-auto"
                >
                  <h3 className="text-sm font-medium text-gray-600 mb-2">
                    Du hast gesagt:
                  </h3>
                  <p className="text-lg text-gray-900">{currentText}</p>
                </motion.div>
              )}
            </AnimatePresence>

            {/* Last Response */}
            <AnimatePresence>
              {lastResponse && (
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -20 }}
                  className="bg-primary-50 border border-primary-200 rounded-2xl p-6 max-w-2xl mx-auto"
                >
                  <h3 className="text-sm font-medium text-primary-600 mb-2">
                    Assistant Antwort:
                  </h3>
                  <p className="text-lg text-primary-900">{lastResponse}</p>
                </motion.div>
              )}
            </AnimatePresence>

            {/* Instructions */}
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.5 }}
              className="text-center text-gray-500 space-y-2"
            >
              <p className="text-sm">
                {isConnected
                  ? "Klicke den Mikrofon-Button und sprich deine Frage"
                  : "Backend nicht verbunden - stelle sicher, dass der Server läuft"}
              </p>
              {isConnected && (
                <div className="flex items-center justify-center space-x-4 text-xs">
                  <span className="flex items-center">
                    <div className="w-2 h-2 bg-blue-400 rounded-full mr-2"></div>
                    Bereit
                  </span>
                  <span className="flex items-center">
                    <div className="w-2 h-2 bg-red-400 rounded-full mr-2"></div>
                    Aufnahme
                  </span>
                  <span className="flex items-center">
                    <div className="w-2 h-2 bg-green-400 rounded-full mr-2"></div>
                    Sprechen
                  </span>
                </div>
              )}
            </motion.div>
          </div>
        </div>
      </motion.div>
    </div>
  );
};

export default VoiceMode;
import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { MessageCircle, Mic, Settings } from 'lucide-react';
import ChatInterface from './components/ChatInterface';
import VoiceMode from './components/VoiceMode';
import './App.css';

function App() {
  const [mode, setMode] = useState('chat'); // 'chat' or 'voice'
  const [isConnected, setIsConnected] = useState(false);

  useEffect(() => {
    // Check backend connection
    checkBackendConnection();
  }, []);

  const checkBackendConnection = async () => {
    try {
      const response = await fetch('http://localhost:8080/health');
      setIsConnected(response.ok);
    } catch (error) {
      setIsConnected(false);
    }
  };

  const toggleMode = () => {
    setMode(mode === 'chat' ? 'voice' : 'chat');
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100">
      {/* Header */}
      <motion.header 
        initial={{ y: -50, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        className="bg-white shadow-sm border-b border-gray-200"
      >
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center space-x-3">
              <div className="w-8 h-8 bg-primary-500 rounded-lg flex items-center justify-center">
                <MessageCircle className="w-5 h-5 text-white" />
              </div>
              <div>
                <h1 className="text-xl font-semibold text-gray-900">Voice Assistant</h1>
                <p className="text-sm text-gray-500">
                  {isConnected ? (
                    <span className="flex items-center">
                      <span className="w-2 h-2 bg-green-400 rounded-full mr-2"></span>
                      Verbunden
                    </span>
                  ) : (
                    <span className="flex items-center">
                      <span className="w-2 h-2 bg-red-400 rounded-full mr-2"></span>
                      Nicht verbunden
                    </span>
                  )}
                </p>
              </div>
            </div>
            
            <div className="flex items-center space-x-4">
              {/* Mode Toggle */}
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={toggleMode}
                className={`flex items-center space-x-2 px-4 py-2 rounded-lg font-medium transition-colors ${
                  mode === 'voice' 
                    ? 'bg-primary-500 text-white' 
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                {mode === 'voice' ? (
                  <>
                    <Mic className="w-4 h-4" />
                    <span>Voice Mode</span>
                  </>
                ) : (
                  <>
                    <MessageCircle className="w-4 h-4" />
                    <span>Chat Mode</span>
                  </>
                )}
              </motion.button>
              
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className="p-2 text-gray-400 hover:text-gray-600 transition-colors"
              >
                <Settings className="w-5 h-5" />
              </motion.button>
            </div>
          </div>
        </div>
      </motion.header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <AnimatePresence mode="wait">
          {mode === 'chat' ? (
            <motion.div
              key="chat"
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: 20 }}
              transition={{ duration: 0.3 }}
            >
              <ChatInterface isConnected={isConnected} />
            </motion.div>
          ) : (
            <motion.div
              key="voice"
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -20 }}
              transition={{ duration: 0.3 }}
            >
              <VoiceMode isConnected={isConnected} />
            </motion.div>
          )}
        </AnimatePresence>
      </main>

      {/* Footer */}
      <motion.footer 
        initial={{ y: 50, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        className="bg-white border-t border-gray-200 mt-auto"
      >
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="text-center text-sm text-gray-500">
            Powered by Custom OpenAI Server, Whisper & XTTS • {mode === 'chat' ? 'Modo Texto' : 'Modo Voz'}
          </div>
        </div>
      </motion.footer>
    </div>
  );
}

export default App;
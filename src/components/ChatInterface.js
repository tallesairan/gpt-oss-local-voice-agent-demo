import React, { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Send, Bot, User, Loader } from 'lucide-react';
import { sendChatMessage } from '../services/api';

const ChatInterface = ({ isConnected }) => {
  const [messages, setMessages] = useState([
    {
      id: 1,
      text: "Hallo! Ich bin dein lokaler Voice Assistant. Wie kann ich dir helfen?",
      sender: 'assistant',
      timestamp: new Date().toLocaleTimeString()
    }
  ]);
  const [inputText, setInputText] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (!inputText.trim() || !isConnected || isLoading) return;

    const userMessage = {
      id: Date.now(),
      text: inputText,
      sender: 'user',
      timestamp: new Date().toLocaleTimeString()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputText('');
    setIsLoading(true);

    try {
      const response = await sendChatMessage(inputText);
      
      const assistantMessage = {
        id: Date.now() + 1,
        text: response.response,
        sender: 'assistant',
        timestamp: new Date().toLocaleTimeString()
      };

      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      const errorMessage = {
        id: Date.now() + 1,
        text: "Entschuldigung, es gab ein Problem bei der Verarbeitung deiner Nachricht. Bitte versuche es erneut.",
        sender: 'assistant',
        timestamp: new Date().toLocaleTimeString(),
        isError: true
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
      inputRef.current?.focus();
    }
  };

  const TypingIndicator = () => (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -10 }}
      className="flex items-center space-x-2 p-4 bg-white rounded-xl mr-auto max-w-xs shadow-sm border border-gray-200"
    >
      <Bot className="w-5 h-5 text-primary-500" />
      <div className="typing-indicator">
        <div className="typing-dot"></div>
        <div className="typing-dot"></div>
        <div className="typing-dot"></div>
      </div>
      <span className="text-sm text-gray-500">Assistant tippt...</span>
    </motion.div>
  );

  const MessageBubble = ({ message }) => (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className={`chat-message ${
        message.sender === 'user' ? 'user-message' : 'assistant-message'
      } ${message.isError ? 'bg-red-50 border-red-200 text-red-800' : ''}`}
    >
      <div className="flex items-start space-x-3">
        <div className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center ${
          message.sender === 'user' 
            ? 'bg-primary-600 text-white' 
            : message.isError 
              ? 'bg-red-100 text-red-600'
              : 'bg-gray-100 text-gray-600'
        }`}>
          {message.sender === 'user' ? (
            <User className="w-4 h-4" />
          ) : (
            <Bot className="w-4 h-4" />
          )}
        </div>
        <div className="flex-1">
          <p className="text-sm font-medium mb-1">
            {message.sender === 'user' ? 'Du' : 'Assistant'}
          </p>
          <p className="text-sm leading-relaxed whitespace-pre-wrap">
            {message.text}
          </p>
          <p className="text-xs opacity-60 mt-2">
            {message.timestamp}
          </p>
        </div>
      </div>
    </motion.div>
  );

  return (
    <div className="max-w-4xl mx-auto">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="bg-white rounded-2xl shadow-lg border border-gray-200 overflow-hidden"
      >
        {/* Chat Header */}
        <div className="bg-gradient-to-r from-primary-500 to-primary-600 p-6 text-white">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 bg-white bg-opacity-20 rounded-full flex items-center justify-center">
              <Bot className="w-6 h-6" />
            </div>
            <div>
              <h2 className="text-xl font-semibold">Chat mit dem Assistant</h2>
              <p className="text-primary-100 text-sm">
                Stelle deine Fragen in deutscher Sprache
              </p>
            </div>
          </div>
        </div>

        {/* Messages Container */}
        <div className="chat-container h-96 overflow-y-auto p-6 space-y-4 bg-gray-50">
          <AnimatePresence>
            {messages.map((message) => (
              <MessageBubble key={message.id} message={message} />
            ))}
            {isLoading && <TypingIndicator />}
          </AnimatePresence>
          <div ref={messagesEndRef} />
        </div>

        {/* Input Form */}
        <div className="border-t border-gray-200 p-6 bg-white">
          <form onSubmit={handleSendMessage} className="flex space-x-4">
            <div className="flex-1">
              <input
                ref={inputRef}
                type="text"
                value={inputText}
                onChange={(e) => setInputText(e.target.value)}
                placeholder={
                  isConnected 
                    ? "Schreibe deine Nachricht..." 
                    : "Backend nicht verbunden..."
                }
                disabled={!isConnected || isLoading}
                className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-transparent disabled:bg-gray-100 disabled:text-gray-500 transition-colors"
              />
            </div>
            <motion.button
              type="submit"
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              disabled={!inputText.trim() || !isConnected || isLoading}
              className="px-6 py-3 bg-primary-500 text-white rounded-xl hover:bg-primary-600 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors flex items-center space-x-2"
            >
              {isLoading ? (
                <Loader className="w-5 h-5 animate-spin" />
              ) : (
                <Send className="w-5 h-5" />
              )}
              <span className="hidden sm:inline">Senden</span>
            </motion.button>
          </form>
          
          {!isConnected && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="mt-4 p-3 bg-yellow-50 border border-yellow-200 rounded-lg"
            >
              <p className="text-sm text-yellow-800">
                ⚠️ Backend nicht erreichbar. Stelle sicher, dass der Python-Server läuft.
              </p>
            </motion.div>
          )}
        </div>
      </motion.div>
    </div>
  );
};

export default ChatInterface;
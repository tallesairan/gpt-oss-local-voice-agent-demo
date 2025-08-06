/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
    "./public/index.html"
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#f0f9ff',
          100: '#e0f2fe',
          200: '#bae6fd',
          300: '#7dd3fc',
          400: '#38bdf8',
          500: '#0ea5e9',
          600: '#0284c7',
          700: '#0369a1',
          800: '#075985',
          900: '#0c4a6e',
        },
        gray: {
          50: '#f9fafb',
          100: '#f3f4f6',
          200: '#e5e7eb',
          300: '#d1d5db',
          400: '#9ca3af',
          500: '#6b7280',
          600: '#4b5563',
          700: '#374151',
          800: '#1f2937',
          900: '#111827',
        }
      },
      animation: {
        'pulse-glow': 'pulse-glow 2s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'voice-wave': 'voice-wave 1.5s ease-in-out infinite',
        'typing': 'typing 1.5s ease-in-out infinite'
      },
      keyframes: {
        'pulse-glow': {
          '0%, 100%': { 
            opacity: '1',
            transform: 'scale(1)',
            boxShadow: '0 0 20px rgba(14, 165, 233, 0.5)'
          },
          '50%': { 
            opacity: '0.8',
            transform: 'scale(1.05)',
            boxShadow: '0 0 40px rgba(14, 165, 233, 0.8)'
          }
        },
        'voice-wave': {
          '0%, 100%': { 
            transform: 'scaleY(1)',
            opacity: '0.7'
          },
          '50%': { 
            transform: 'scaleY(1.5)',
            opacity: '1'
          }
        },
        'typing': {
          '0%, 50%': { opacity: '1' },
          '51%, 100%': { opacity: '0' }
        }
      }
    },
  },
  plugins: [],
}
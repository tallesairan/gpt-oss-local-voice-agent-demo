const API_BASE_URL = 'http://localhost:8080';

class APIError extends Error {
  constructor(message, status) {
    super(message);
    this.status = status;
    this.name = 'APIError';
  }
}

const apiRequest = async (endpoint, options = {}) => {
  try {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new APIError(
        errorData.error || `HTTP ${response.status}: ${response.statusText}`,
        response.status
      );
    }

    return await response.json();
  } catch (error) {
    if (error instanceof APIError) {
      throw error;
    }
    // Network or other errors
    throw new APIError(
      'Verbindung zum Backend fehlgeschlagen. Ist der Server gestartet?',
      0
    );
  }
};

// Chat API
export const sendChatMessage = async (message) => {
  return await apiRequest('/chat', {
    method: 'POST',
    body: JSON.stringify({ message }),
  });
};

// Voice API
export const startRecording = async () => {
  return await apiRequest('/voice/start', {
    method: 'POST',
  });
};

export const stopRecording = async () => {
  return await apiRequest('/voice/stop', {
    method: 'POST',
  });
};

export const getCurrentStatus = async () => {
  return await apiRequest('/voice/status');
};

// Health check
export const checkHealth = async () => {
  return await apiRequest('/health');
};

// Configuration
export const getConfig = async () => {
  return await apiRequest('/config');
};

export const updateConfig = async (config) => {
  return await apiRequest('/config', {
    method: 'PUT',
    body: JSON.stringify(config),
  });
};

export default {
  sendChatMessage,
  startRecording,
  stopRecording,
  getCurrentStatus,
  checkHealth,
  getConfig,
  updateConfig,
};
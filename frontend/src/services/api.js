import axios from 'axios';

// Base API URL with fallback
const API_BASE = '/api/v1';

const apiClient = axios.create({
  baseURL: API_BASE,
  timeout: 20000,
});

// Request interceptor to attach JWT token
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('smart_kisan_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      // Clear token if expired/invalid
      localStorage.removeItem('smart_kisan_token');
    }
    return Promise.reject(error);
  }
);

export const api = {
  // Auth
  login: async (phone, password) => {
    const response = await apiClient.post('/auth/login', { phone, password });
    return response.data;
  },

  register: async (phone, fullName, preferredLanguage = 'en', password) => {
    const response = await apiClient.post('/auth/register', {
      phone,
      full_name: fullName,
      preferred_language: preferredLanguage,
      password,
    });
    return response.data;
  },

  getMe: async () => {
    const response = await apiClient.get('/auth/me');
    return response.data;
  },

  updateProfile: async (profileData) => {
    const response = await apiClient.put('/auth/profile', profileData);
    return response.data;
  },

  // Disease Detection
  predictDisease: async (file) => {
    const formData = new FormData();
    formData.append('image', file);
    const response = await apiClient.post('/predict/disease', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  getDiseaseHistory: async () => {
    const response = await apiClient.get('/predict/disease/history');
    return response.data;
  },

  // Crop Recommendation
  recommendCrop: async (cropData) => {
    const response = await apiClient.post('/recommend/crop', cropData);
    return response.data;
  },

  // Weather Advisory
  getWeather: async (lat, lon) => {
    const response = await apiClient.get('/weather', {
      params: { lat, lon },
    });
    return response.data;
  },

  // Market Prices
  getCommodities: async () => {
    const response = await apiClient.get('/market/commodities');
    return response.data;
  },

  getMarketPrices: async (commodity, state = '') => {
    const params = { commodity };
    if (state && state !== 'All States') {
      params.state = state;
    }
    const response = await apiClient.get('/market/prices', { params });
    return response.data;
  },

  // Government Schemes
  getSchemes: async (params = {}) => {
    const response = await apiClient.get('/schemes', { params });
    return response.data;
  },

  // AI Chat (Krishi Mitra)
  sendChatMessage: async (message, sessionId, language = 'en') => {
    const response = await apiClient.post('/chat', {
      message,
      session_id: sessionId,
      language,
    });
    return response.data;
  },

  // History
  getHistory: async (type = 'all') => {
    const response = await apiClient.get('/history', {
      params: { type },
    });
    return response.data;
  },
};

export default api;

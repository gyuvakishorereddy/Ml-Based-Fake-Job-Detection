import axios from 'axios'

// Create axios instance with default config
const API = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:5000/api',
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor
API.interceptors.request.use(
  (config) => {
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor
API.interceptors.response.use(
  (response) => {
    return response
  },
  (error) => {
    console.error('API Error:', error)
    return Promise.reject(error)
  }
)

// API functions
export const predictJob = async (data) => {
  try {
    const response = await API.post('/predict-job', data)
    return response.data
  } catch (error) {
    throw error.response?.data || error.message
  }
}

export const predictInternship = async (data) => {
  try {
    const response = await API.post('/predict-internship', data)
    return response.data
  } catch (error) {
    throw error.response?.data || error.message
  }
}

export const analyzeText = async (data) => {
  try {
    const response = await API.post('/analyze-text', data)
    return response.data
  } catch (error) {
    throw error.response?.data || error.message
  }
}

export const comprehensiveAnalysis = async (data) => {
  try {
    const response = await API.post('/comprehensive-analysis', data)
    return response.data
  } catch (error) {
    throw error.response?.data || error.message
  }
}

export const checkHealth = async () => {
  try {
    const response = await API.get('/health')
    return response.data
  } catch (error) {
    throw error.response?.data || error.message
  }
}

export default API

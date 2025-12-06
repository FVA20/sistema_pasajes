import axios from 'axios';

const API_URL = 'http://127.0.0.1:8000';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor para agregar token si existe
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

export default api;

// Funciones para la API
export const pasajesAPI = {
  // Obtener todos los pasajes
  getAll: () => api.get('/api/pasajes/'),
  
  // Obtener un pasaje por ID
  getById: (id) => api.get(`/api/pasajes/${id}/`),
  
  // Crear nuevo pasaje
  create: (data) => api.post('/api/pasajes/', data),
  
  // Buscar pasajes por fecha
  buscarPorFecha: (fecha) => api.get(`/api/pasajes/?fecha_viaje=${fecha}`),
  
  // Obtener asientos disponibles
  getAsientosDisponibles: (fecha, hora) => 
    api.get(`/api/asientos-disponibles/?fecha=${fecha}&hora=${hora}`),
};

export const pasajerosAPI = {
  // Obtener todos los pasajeros
  getAll: () => api.get('/api/pasajeros/'),
  
  // Crear nuevo pasajero
  create: (data) => api.post('/api/pasajeros/', data),
  
  // Buscar por DNI
  buscarPorDNI: (dni) => api.get(`/api/pasajeros/?dni=${dni}`),
};
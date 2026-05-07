import axios from 'axios';

const explicitBase = import.meta.env.VITE_API_BASE_URL;
const apiHost = import.meta.env.VITE_API_URL;
const baseURL = explicitBase || (apiHost ? `${apiHost}/api` : '/api');

const api = axios.create({
  baseURL,
  headers: {
    'Content-Type': 'application/json',
  },
});

let refreshPromise = null;

const clearAuth = () => {
  localStorage.removeItem('access_token');
  localStorage.removeItem('refresh_token');
  if (window.location.pathname !== '/') {
    window.location.assign('/');
  }
};

const refreshAccessToken = async () => {
  const refreshToken = localStorage.getItem('refresh_token');
  if (!refreshToken) {
    throw new Error('No refresh token available');
  }

  const response = await api.post(
    '/auth/refresh',
    { refresh_token: refreshToken },
    { skipAuthRefresh: true }
  );

  const { access_token: accessToken, refresh_token: newRefreshToken } = response.data;
  localStorage.setItem('access_token', accessToken);
  localStorage.setItem('refresh_token', newRefreshToken);
  return accessToken;
};

api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const status = error.response?.status;
    const originalRequest = error.config || {};
    const requestUrl = originalRequest.url || '';

    if (status !== 401) {
      return Promise.reject(error);
    }

    if (requestUrl.includes('/auth/login')) {
      return Promise.reject(error);
    }

    if (originalRequest.skipAuthRefresh || requestUrl.includes('/auth/refresh')) {
      clearAuth();
      return Promise.reject(error);
    }

    if (originalRequest._retry) {
      clearAuth();
      return Promise.reject(error);
    }

    originalRequest._retry = true;

    try {
      if (!refreshPromise) {
        refreshPromise = refreshAccessToken().finally(() => {
          refreshPromise = null;
        });
      }

      const newAccessToken = await refreshPromise;
      originalRequest.headers = originalRequest.headers || {};
      originalRequest.headers.Authorization = `Bearer ${newAccessToken}`;
      return api(originalRequest);
    } catch (refreshError) {
      clearAuth();
      return Promise.reject(refreshError);
    }
  }
);

export default api;

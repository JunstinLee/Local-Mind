import axios from 'axios';

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '/api',
});

// 获取后端服务状态
export const getStatus = async () => {
  try {
    const response = await apiClient.get('/status/backend');
    return response.data;
  } catch (error) {
    console.error('Error fetching backend status:', error);
    throw error;
  }
};
import axios from 'axios';

// Get the current host (works in both dev and inspection mode)
const currentHost = window.location.hostname;
const API_BASE_URL = import.meta.env.DEV 
  ? `http://${currentHost}:8000/api/v1`  // Dynamic host
  : '/api/v1';

console.log('Using API URL:', API_BASE_URL); // Debug log

// Create axios instance
export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true,
  timeout: 5000, // Add timeout
});

// Add request interceptor to handle errors
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    console.error('Request error:', error);
    return Promise.reject(error);
  }
);

// Add response interceptor for debugging
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error);
    return Promise.reject(error);
  }
);

export interface LoginData {
  email: string;
  password: string;
}

export interface RegisterData extends LoginData {
  full_name: string;
}

export const auth = {
  login: async (data: LoginData) => {
    const response = await api.post('/auth/login', data);
    return response.data;
  },
  register: async (data: RegisterData) => {
    const response = await api.post('/auth/register', data);
    return response.data;
  },
};

export interface User {
  id: number;
  email: string;
  full_name: string;
}

export interface Article {
  id: number;
  title: string;
  content: string;
  summary: string | null;
  tags: string[];
  status: 'draft' | 'published';
  author_id: number;
  author: User;
  comment_count: number;
  created_at: string;
}

export interface CreateArticleData {
  title: string;
  content: string;
  summary?: string;
  tags: string[];
  status: 'draft' | 'published';
}

export const articles = {
  list: async (page = 1, size = 10) => {
    const response = await api.get(`/articles?page=${page}&size=${size}`);
    return response.data;
  },
  
  get: async (id: number) => {
    const response = await api.get(`/articles/${id}`);
    return response.data;
  },
  
  create: async (data: CreateArticleData) => {
    const response = await api.post('/articles', data);
    return response.data;
  },
  
  update: async (id: number, data: Partial<CreateArticleData>) => {
    const response = await api.patch(`/articles/${id}`, data);
    return response.data;
  },
  
  delete: async (id: number) => {
    const response = await api.delete(`/articles/${id}`);
    return response.data;
  },
};

export interface Comment {
  id: number;
  content: string;
  article_id: number;
  author_id: number;
  author: User;
  created_at: string;
  updated_at: string;
}

export interface CreateCommentData {
  content: string;
}

export const comments = {
  list: async (articleId: number) => {
    console.log('Fetching comments for article:', articleId);
    const response = await api.get(`/comments/article/${articleId}`);
    console.log('Comments response:', response.data);
    return response.data;
  },
  
  create: async (articleId: number, data: CreateCommentData) => {
    console.log('Creating comment:', { articleId, data });
    const response = await api.post(`/comments`, {
      content: data.content,
      article_id: articleId
    });
    console.log('Create comment response:', response.data);
    return response.data;
  },
}; 
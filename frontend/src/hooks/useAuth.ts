import { useEffect, useState } from 'react';
import { api } from '../lib/api';

interface User {
  id: number;
  email: string;
  full_name: string;
  article_count: number;
  comment_count: number;
  created_at: string;
  recent_articles: any[];
  recent_comments: any[];
}

export function useAuth() {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const token = localStorage.getItem('token');

  useEffect(() => {
    const fetchUser = async () => {
      if (!token) {
        setLoading(false);
        return;
      }

      try {
        const response = await api.get('/users/me');
        setUser(response.data);
      } catch (error) {
        console.error('Failed to fetch user:', error);
        localStorage.removeItem('token');
      } finally {
        setLoading(false);
      }
    };

    fetchUser();
  }, [token]);

  return {
    user,
    loading,
    isAuthenticated: !!token,
  };
} 
import { useState } from 'react';
import { auth, RegisterData } from '../../lib/api';
import { Link, useNavigate } from 'react-router-dom';
import { PageContainer } from '../../components/PageContainer';

export function RegisterForm() {
  const [formData, setFormData] = useState<RegisterData>({
    email: '',
    password: '',
    full_name: '',
  });
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setIsLoading(true);

    console.log('Form submitted with data:', formData);
    console.log('API URL:', import.meta.env.DEV ? 'http://192.168.1.101:8000/api/v1' : '/api/v1');

    try {
      console.log('Attempting registration...');
      const response = await auth.register(formData);
      console.log('Registration response:', response);

      try {
        console.log('Attempting auto-login...');
        const loginResponse = await auth.login({
          email: formData.email,
          password: formData.password,
        });
        console.log('Login response:', loginResponse);
        localStorage.setItem('token', loginResponse.access_token);
        navigate('/');
      } catch (loginErr: any) {
        console.error('Auto-login error:', loginErr);
        console.error('Login error details:', loginErr.response?.data);
        setError('Registration successful but login failed. Please try logging in manually.');
        navigate('/login');
      }
    } catch (err: any) {
      console.error('Registration error:', err);
      console.error('Error type:', err.constructor.name);
      console.error('Error message:', err.message);
      console.error('Response data:', err.response?.data);
      setError(
        err.response?.data?.detail || 
        'Registration failed. Please try again.'
      );
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <PageContainer>
      <div className="max-w-md mx-auto">
        <h2 className="text-2xl font-bold mb-6 text-center text-gray-800">Register</h2>
        {error && (
          <div className="mb-4 p-3 bg-red-50 text-red-700 rounded-lg text-sm">
            {error}
          </div>
        )}
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label htmlFor="full_name" className="block text-sm font-medium text-gray-700">
              Full Name
            </label>
            <input
              id="full_name"
              type="text"
              className="input"
              value={formData.full_name}
              onChange={(e) => setFormData({ ...formData, full_name: e.target.value })}
              disabled={isLoading}
              required
            />
          </div>
          <div>
            <label htmlFor="email" className="block text-sm font-medium text-gray-700">
              Email
            </label>
            <input
              id="email"
              type="email"
              className="input"
              value={formData.email}
              onChange={(e) => setFormData({ ...formData, email: e.target.value })}
              disabled={isLoading}
              required
            />
          </div>
          <div>
            <label htmlFor="password" className="block text-sm font-medium text-gray-700">
              Password
            </label>
            <input
              id="password"
              type="password"
              className="input"
              value={formData.password}
              onChange={(e) => setFormData({ ...formData, password: e.target.value })}
              disabled={isLoading}
              required
            />
          </div>
          <button 
            type="submit" 
            className="btn btn-primary w-full disabled:opacity-50"
            disabled={isLoading}
          >
            {isLoading ? 'Registering...' : 'Register'}
          </button>
        </form>
        <p className="mt-4 text-center text-sm text-gray-600">
          Already have an account?{' '}
          <Link to="/login" className="text-primary-600 hover:text-primary-700">
            Login
          </Link>
        </p>
      </div>
    </PageContainer>
  );
} 
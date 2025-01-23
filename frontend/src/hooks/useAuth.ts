import { useState } from 'react';
import { api } from '../services/api';
import { useNavigate } from 'react-router-dom';

export const useAuth = () => {
    const [error, setError] = useState<string | null>(null);
    const navigate = useNavigate();

    const login = async (email: string, password: string) => {
        try {
            const response = await api.post('/auth/login/', { email, password });
            localStorage.setItem('token', response.data.token);
            api.defaults.headers.common['Authorization'] = `Bearer ${response.data.token}`;
            navigate('/dashboard');
        } catch (err) {
            setError('Invalid credentials');
        }
    };

    const logout = () => {
        localStorage.removeItem('token');
        delete api.defaults.headers.common['Authorization'];
        navigate('/login');
    };

    return { login, logout, error };
}; 
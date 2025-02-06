import { useState } from 'react';

interface User {
  id: string;
  name: string;
  email: string;
}

interface SignInCredentials {
  email: string;
  password: string;
}

interface SignUpCredentials extends SignInCredentials {
  name: string;
}

export function useAuth() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [user, setUser] = useState<User | null>(null);

  const signIn = async (credentials: SignInCredentials) => {
    try {
      // Replace with actual API call
      const response = await fetch('/api/auth/signin', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(credentials),
      });
      
      if (!response.ok) throw new Error('Invalid credentials');
      
      const data = await response.json();
      setUser(data.user);
      setIsAuthenticated(true);
      localStorage.setItem('token', data.token);
    } catch (error) {
      throw error;
    }
  };

  const signUp = async (credentials: SignUpCredentials) => {
    try {
      // Replace with actual API call
      const response = await fetch('/api/auth/signup', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(credentials),
      });
      
      if (!response.ok) throw new Error('Failed to create account');
      
      const data = await response.json();
      setUser(data.user);
      setIsAuthenticated(true);
      localStorage.setItem('token', data.token);
    } catch (error) {
      throw error;
    }
  };

  const signOut = async () => {
    try {
      // Add API call to backend logout endpoint here
      await fetch('/api/auth/signout', { method: 'POST' });
      localStorage.removeItem('token');
      sessionStorage.clear();
      setUser(null);
      setIsAuthenticated(false);
    } catch (error) {
      throw error;
    }
  };

  const resetPassword = async (email: string) => {
    try {
      // Replace with actual API call
      const response = await fetch('/api/auth/reset-password', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email }),
      });
      
      if (!response.ok) throw new Error('Failed to send reset instructions');
    } catch (error) {
      throw error;
    }
  };

  return {
    user,
    isAuthenticated,
    signIn,
    signUp,
    signOut,
    resetPassword,
  };
} 
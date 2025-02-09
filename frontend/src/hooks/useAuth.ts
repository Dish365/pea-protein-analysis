import { useState } from "react";
import { useMutation } from "@tanstack/react-query";
import axios from "axios";
import { API_BASE_URL, API_ENDPOINTS } from "@/config/api";

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

  const signIn = async (credentials: { email: string; password: string }) => {
    const response = await axios.post(
      `${API_BASE_URL}${API_ENDPOINTS.auth.signIn}`,
      credentials
    );
    const { access, refresh } = response.data;
    localStorage.setItem("token", access);
    localStorage.setItem("refreshToken", refresh);
    return response.data;
  };

  const signUp = async (credentials: SignUpCredentials) => {
    try {
      // Replace with actual API call
      const response = await fetch("/api/auth/signup", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(credentials),
      });

      if (!response.ok) throw new Error("Failed to create account");

      const data = await response.json();
      setUser(data.user);
      setIsAuthenticated(true);
      localStorage.setItem("token", data.token);
    } catch (error) {
      throw error;
    }
  };

  const signOut = async () => {
    try {
      // Add API call to backend logout endpoint here
      await fetch("/api/auth/signout", { method: "POST" });
      localStorage.removeItem("token");
      localStorage.removeItem("refreshToken");
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
      const response = await fetch("/api/auth/reset-password", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email }),
      });

      if (!response.ok) throw new Error("Failed to send reset instructions");
    } catch (error) {
      throw error;
    }
  };

  // Add refresh token logic
  const refreshToken = async () => {
    const refresh = localStorage.getItem("refreshToken");
    if (!refresh) throw new Error("No refresh token");

    const response = await axios.post(
      `${API_BASE_URL}${API_ENDPOINTS.auth.refreshToken}`,
      { refresh }
    );

    localStorage.setItem("token", response.data.access);
    return response.data;
  };

  return {
    user,
    isAuthenticated,
    signIn,
    signUp,
    signOut,
    resetPassword,
    refreshToken,
  };
}

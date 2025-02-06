import { useState, useEffect } from "react";
import { message } from "antd";

interface User {
  id: string;
  name: string;
  email: string;
  role: string;
  organization?: string;
  jobTitle?: string;
}

export function useUser() {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchUser();
  }, []);

  const fetchUser = async () => {
    try {
      // Replace with actual API call
      const response = await fetch("/api/user");
      const data = await response.json();
      setUser(data);
    } catch (error) {
      message.error("Failed to fetch user data");
    } finally {
      setLoading(false);
    }
  };

  const updateUser = async (userData: Partial<User>) => {
    try {
      // Replace with actual API call
      const response = await fetch("/api/user", {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(userData),
      });
      const data = await response.json();
      setUser(data);
      return data;
    } catch (error) {
      throw new Error("Failed to update user data");
    }
  };

  return { user, loading, updateUser };
} 
import { useState, useEffect } from "react";
import { useToast } from "@/hooks/useToast";

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
  const { toast } = useToast();

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
      toast({
        title: "Error",
        description: "Failed to fetch user data",
        variant: "destructive",
      });
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
      toast({
        title: "Success",
        description: "User data updated successfully",
      });
      return data;
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to update user data",
        variant: "destructive",
      });
      throw new Error("Failed to update user data");
    }
  };

  return { user, loading, updateUser };
} 
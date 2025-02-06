import { useState, useEffect } from "react";
import { message } from "antd";

interface Settings {
  defaultProcessType: string;
  cacheDuration: number;
  autoRefresh: boolean;
  refreshInterval: number;
  theme: "light" | "dark" | "system";
  defaultChartType: string;
  showTooltips: boolean;
  emailNotifications: boolean;
  completionAlerts: boolean;
  errorNotifications: boolean;
}

export function useSettings() {
  const [settings, setSettings] = useState<Settings>({
    defaultProcessType: "baseline",
    cacheDuration: 30,
    autoRefresh: true,
    refreshInterval: 10,
    theme: "system",
    defaultChartType: "bar",
    showTooltips: true,
    emailNotifications: true,
    completionAlerts: true,
    errorNotifications: true,
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchSettings();
  }, []);

  const fetchSettings = async () => {
    try {
      // Replace with actual API call
      const response = await fetch("/api/settings");
      const data = await response.json();
      setSettings(data);
    } catch (error) {
      message.error("Failed to fetch settings");
    } finally {
      setLoading(false);
    }
  };

  const updateSettings = async (newSettings: Partial<Settings>) => {
    try {
      // Replace with actual API call
      const response = await fetch("/api/settings", {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(newSettings),
      });
      const data = await response.json();
      setSettings(data);
      return data;
    } catch (error) {
      throw new Error("Failed to update settings");
    }
  };

  return { settings, loading, updateSettings };
} 
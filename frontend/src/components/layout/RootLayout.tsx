"use client";

import React, { useEffect, useState } from "react";
import { Layout, ConfigProvider, theme } from "antd";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import Navigation from "./Navigation";
import { usePathname } from "next/navigation";
import LoadingSpinner from "../common/LoadingSpinner";

const { Content } = Layout;

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
    },
  },
});

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const pathname = usePathname();
  const [isLoading, setIsLoading] = useState(true); // Start with loading true
  const [isInitialLoad, setIsInitialLoad] = useState(true); // Track initial load

  useEffect(() => {
    // Handle initial load
    if (isInitialLoad) {
      const timer = setTimeout(() => {
        setIsInitialLoad(false);
        setIsLoading(false);
      }, 1500); // Longer delay for initial load
      return () => clearTimeout(timer);
    }

    // Handle subsequent route changes
    setIsLoading(true);
    const timer = setTimeout(() => {
      setIsLoading(false);
    }, 500);
    return () => clearTimeout(timer);
  }, [pathname, isInitialLoad]);

  if (isInitialLoad || isLoading) {
    return (
      <LoadingSpinner
        tip={isInitialLoad ? "Starting application..." : "Loading content..."}
      />
    );
  }

  return (
    <QueryClientProvider client={queryClient}>
      <ConfigProvider
        theme={{
          algorithm: theme.defaultAlgorithm,
          token: {
            colorPrimary: "#0ea5e9",
            borderRadius: 6,
          },
        }}
      >
        <Layout className="min-h-screen">
          <Navigation />
          <Content className="p-6 bg-gray-50">
            <div className="max-w-7xl mx-auto">{children}</div>
          </Content>
        </Layout>
      </ConfigProvider>
    </QueryClientProvider>
  );
}

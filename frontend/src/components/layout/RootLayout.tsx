"use client";

import React from 'react';
import { Layout, ConfigProvider, theme } from 'antd';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import Navigation from './Navigation';

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
  return (
    <QueryClientProvider client={queryClient}>
      <ConfigProvider
        theme={{
          algorithm: theme.defaultAlgorithm,
          token: {
            colorPrimary: '#0ea5e9',
            borderRadius: 6,
          },
        }}
      >
        <Layout className="min-h-screen">
          <Navigation />
          <Content className="p-6 bg-gray-50">
            <div className="max-w-7xl mx-auto">
              {children}
            </div>
          </Content>
        </Layout>
      </ConfigProvider>
    </QueryClientProvider>
  );
} 
"use client";

import RootLayout from '@/components/layout/RootLayout';
import '@/styles/globals.css';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { useState } from 'react';
import { App as AntApp } from 'antd';

export default function Layout({
  children,
}: {
  children: React.ReactNode;
}) {
  const [queryClient] = useState(() => new QueryClient());

  return (
    <html lang="en">
      <body>
        <QueryClientProvider client={queryClient}>
          <AntApp>
            <RootLayout>{children}</RootLayout>
          </AntApp>
        </QueryClientProvider>
      </body>
    </html>
  );
} 
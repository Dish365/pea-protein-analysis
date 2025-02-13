"use client";

import { AuthProvider } from "./auth";
import { QueryProvider } from "./query";

export function Providers({ children }: { children: React.ReactNode }) {
  return (
    <QueryProvider>
      <AuthProvider>
        {children}
      </AuthProvider>
    </QueryProvider>
  );
} 
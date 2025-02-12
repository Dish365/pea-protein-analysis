"use client";

import React, { useEffect, useState } from "react";
import { usePathname } from "next/navigation";
import { QueryClientProvider } from "@tanstack/react-query";
import { Navigation } from "./Navigation";
import { LoadingSpinner } from "@/components/ui/loading-spinner";
import { queryClient } from "@/lib/query";

export function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const pathname = usePathname();
  const [isLoading, setIsLoading] = useState(true);
  const [isInitialLoad, setIsInitialLoad] = useState(true);

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
      <div className="min-h-screen bg-background">
        <LoadingSpinner
          fullscreen
          tip={isInitialLoad ? "Starting application..." : "Loading content..."}
        />
      </div>
    );
  }

  return (
    <QueryClientProvider client={queryClient}>
      <div className="min-h-screen bg-background">
        <Navigation />
        <main className="container py-6">
          {children}
        </main>
      </div>
    </QueryClientProvider>
  );
}

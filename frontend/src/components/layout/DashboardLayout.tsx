"use client";

import React from "react";
import { TopNav } from "./TopNav";
import { Navigation } from "./Navigation";
import { usePathname } from "next/navigation";
import { cn } from "@/lib/utils";

interface DashboardLayoutProps {
  children: React.ReactNode;
}

export default function DashboardLayout({ children }: DashboardLayoutProps) {
  const pathname = usePathname();
  const isAnalysisPage = pathname.includes('/analysis/');
  const showNavigation = !isAnalysisPage || pathname === '/analysis/history';

  return (
    <div className="min-h-screen bg-background">
      <TopNav />
      <div className="flex flex-col">
        {showNavigation && <Navigation />}
        <main className={cn(
          "flex-1 p-8 pt-6",
          showNavigation ? "container mx-auto" : "px-4"
        )}>
          {children}
        </main>
      </div>
    </div>
  );
}

"use client";

import React from "react";
import { TopNav } from "./TopNav";
import { Navigation } from "./Navigation";

interface DashboardLayoutProps {
  children: React.ReactNode;
}

export default function DashboardLayout({ children }: DashboardLayoutProps) {
  return (
    <div className="min-h-screen flex">
      {/* Side Navigation */}
      <Navigation className="w-64 hidden md:block border-r bg-muted/10" />

      {/* Main Content */}
      <div className="flex-1 flex flex-col">
        <TopNav />
        <main className="flex-1 overflow-auto">
          <div className="container max-w-7xl mx-auto p-6 space-y-8">
            {children}
          </div>
        </main>
      </div>
    </div>
  );
}

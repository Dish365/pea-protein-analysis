"use client";

import React from "react";
import { SideNav } from "./SideNav";
import { TopNav } from "./TopNav";

interface DashboardLayoutProps {
  children: React.ReactNode;
}

export default function DashboardLayout({ children }: DashboardLayoutProps) {
  return (
    <div className="min-h-screen bg-background">
      <TopNav />
      <div className="flex">
        <SideNav />
        <main className="flex-1 p-8 pt-6">
          {children}
        </main>
      </div>
    </div>
  );
}

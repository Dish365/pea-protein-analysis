"use client";

import React from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { cn } from "@/lib/utils";
import {
  BarChart2,
  Activity,
  DollarSign,
  Leaf,
} from "lucide-react";

const menuItems = [
  {
    key: "/dashboard",
    icon: BarChart2,
    label: "Dashboard",
  },
  {
    key: "/dashboard/analysis/technical",
    icon: Activity,
    label: "Technical Analysis",
  },
  {
    key: "/dashboard/analysis/economic",
    icon: DollarSign,
    label: "Economic Analysis",
  },
  {
    key: "/dashboard/analysis/environmental",
    icon: Leaf,
    label: "Environmental Analysis",
  },
];

export function Navigation() {
  const pathname = usePathname();

  return (
    <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container flex h-14 items-center justify-between">
        <Link href="/dashboard" className="flex items-center space-x-2">
          <span className="text-xl font-bold">PEA Protein Analysis</span>
        </Link>

        <nav className="flex items-center space-x-6">
          {menuItems.map((item) => {
            const isActive = pathname === item.key;
            const Icon = item.icon;
            
            return (
              <Link
                key={item.key}
                href={item.key}
                className={cn(
                  "flex items-center space-x-2 text-sm font-medium transition-colors",
                  isActive
                    ? "text-primary"
                    : "text-muted-foreground hover:text-primary"
                )}
              >
                <Icon className="h-4 w-4" />
                <span>{item.label}</span>
              </Link>
            );
          })}
        </nav>
      </div>
    </header>
  );
}

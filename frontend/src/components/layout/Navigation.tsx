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
  History,
  Settings,
  FlaskConical,
  LucideIcon,
} from "lucide-react";

interface MenuItem {
  key: string;
  icon: LucideIcon;
  label: string;
  description?: string;
}

interface MenuDivider {
  type: 'divider';
}

type MenuItemOrDivider = MenuItem | MenuDivider;

const menuItems: MenuItemOrDivider[] = [
  {
    key: "/dashboard",
    icon: BarChart2,
    label: "Dashboard",
  },
  {
    key: "/analysis/new",
    icon: FlaskConical,
    label: "New Analysis",
  },
  {
    key: "/analysis/history",
    icon: History,
    label: "Analysis History",
  },
  {
    type: "divider",
  },
  {
    key: "/analysis/technical",
    icon: Activity,
    label: "Technical Analysis",
    description: "Process efficiency metrics",
  },
  {
    key: "/analysis/economic",
    icon: DollarSign,
    label: "Economic Analysis",
    description: "Cost and profitability analysis",
  },
  {
    key: "/analysis/environmental",
    icon: Leaf,
    label: "Environmental Analysis",
    description: "Environmental impact assessment",
  },
  {
    type: "divider",
  },
  {
    key: "/settings",
    icon: Settings,
    label: "Settings",
  },
];

export function Navigation() {
  const pathname = usePathname();

  const isActiveLink = (path: string) => {
    if (path === "/dashboard") {
      return pathname === path;
    }
    return pathname.startsWith(path);
  };

  const navigationItems = menuItems.filter((item): item is MenuItem => !('type' in item));

  return (
    <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container flex h-14 items-center justify-between">
        <Link href="/dashboard" className="flex items-center space-x-2">
          <span className="text-xl font-bold">PEA Protein Analysis</span>
        </Link>

        <nav className="flex items-center space-x-6">
          {navigationItems.map((item) => {
            const isActive = isActiveLink(item.key);
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

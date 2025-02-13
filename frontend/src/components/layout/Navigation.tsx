"use client";

import React from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import {
  BarChart3,
  FileText,
  History,
  Home,
  Settings,
} from "lucide-react";

interface NavigationProps {
  className?: string;
}

const navigationItems = [
  {
    title: "Overview",
    href: "/dashboard",
    icon: Home,
  },
  {
    title: "New Analysis",
    href: "/dashboard/analysis",
    icon: FileText,
  },
  {
    title: "History",
    href: "/dashboard/history",
    icon: History,
  },
  {
    title: "Reports",
    href: "/dashboard/reports",
    icon: BarChart3,
  },
  {
    title: "Settings",
    href: "/dashboard/settings",
    icon: Settings,
  },
];

export function Navigation({ className }: NavigationProps) {
  const pathname = usePathname();

  return (
    <nav className={cn("py-4", className)}>
      <div className="px-3 py-2">
        <div className="space-y-1">
          {navigationItems.map((item) => {
            const isActive = pathname === item.href;
            return (
              <Link key={item.href} href={item.href}>
                <Button
                  variant={isActive ? "secondary" : "ghost"}
                  className={cn(
                    "w-full justify-start gap-3",
                    isActive ? "bg-primary/10 hover:bg-primary/20" : "hover:bg-muted"
                  )}
                >
                  <item.icon className={cn(
                    "h-4 w-4",
                    isActive ? "text-primary" : "text-muted-foreground"
                  )} />
                  <span className={cn(
                    "text-sm font-medium",
                    isActive ? "text-primary" : "text-muted-foreground"
                  )}>
                    {item.title}
                  </span>
                </Button>
              </Link>
            );
          })}
        </div>
      </div>
    </nav>
  );
}

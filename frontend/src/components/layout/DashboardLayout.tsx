"use client";

import React from "react";
import { Navigation } from "./Navigation";
import { Button } from "@/components/ui/button";
import { Menu } from "lucide-react";
import {
  Sheet,
  SheetContent,
  SheetTrigger,
} from "@/components/ui/sheet";
import { MotionDiv, fadeIn } from "@/components/motion";

interface DashboardLayoutProps {
  children: React.ReactNode;
}

export default function DashboardLayout({ children }: DashboardLayoutProps) {
  const [isMobileNavOpen, setIsMobileNavOpen] = React.useState(false);

  return (
    <div className="relative min-h-screen flex bg-muted/5">
      {/* Background Effects */}
      <div className="fixed inset-0 bg-grid-black/[0.02] -z-10" />
      <div className="fixed inset-0 bg-gradient-to-br from-blue-50/50 via-background to-emerald-50/50 dark:from-blue-950/20 dark:via-background dark:to-emerald-950/20 -z-10" />
      
      {/* Animated Background Orbs */}
      <MotionDiv
        className="fixed top-1/4 right-1/4 w-96 h-96 bg-blue-500/10 rounded-full blur-3xl"
        animate={{
          scale: [1, 1.1, 1],
          opacity: [0.2, 0.3, 0.2],
        }}
        transition={{
          duration: 10,
          repeat: Infinity,
          ease: "easeInOut"
        }}
      />
      <MotionDiv
        className="fixed bottom-1/4 left-1/4 w-96 h-96 bg-emerald-500/10 rounded-full blur-3xl"
        animate={{
          scale: [1.1, 1, 1.1],
          opacity: [0.2, 0.3, 0.2],
        }}
        transition={{
          duration: 10,
          repeat: Infinity,
          ease: "easeInOut",
          delay: 2
        }}
      />

      {/* Desktop Navigation */}
      <Navigation className="w-64 hidden lg:block border-r bg-background/60 backdrop-blur-sm supports-[backdrop-filter]:bg-background/40" />

      {/* Mobile Navigation */}
      <Sheet open={isMobileNavOpen} onOpenChange={setIsMobileNavOpen}>
        <SheetTrigger asChild>
          <Button
            variant="ghost"
            size="icon"
            className="lg:hidden fixed top-4 left-4 z-50 hover:bg-background/80 backdrop-blur-sm"
          >
            <Menu className="h-5 w-5" />
            <span className="sr-only">Toggle navigation menu</span>
          </Button>
        </SheetTrigger>
        <SheetContent 
          side="left" 
          className="w-64 p-0 bg-background/80 backdrop-blur-md"
        >
          <Navigation className="border-none" />
        </SheetContent>
      </Sheet>

      {/* Main Content */}
      <div className="flex-1 flex flex-col min-h-screen">
        <main className="flex-1 relative">
          <MotionDiv
            {...fadeIn}
            transition={{ duration: 0.4 }}
            className="container max-w-7xl mx-auto p-4 md:p-6 lg:p-8 space-y-8"
          >
            {children}
          </MotionDiv>
        </main>
      </div>
    </div>
  );
}

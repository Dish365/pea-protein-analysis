import React from 'react';
import { Card } from "@/components/ui/card";
import { LineChart, ArrowRight, Home } from 'lucide-react';
import Link from 'next/link';
import { Button } from "@/components/ui/button";

interface AnalysisLayoutProps {
  children: React.ReactNode;
}

export default function AnalysisLayout({ children }: AnalysisLayoutProps) {
  return (
    <div className="container mx-auto py-8 space-y-6 animate-in fade-in duration-500">
      <div className="flex items-center gap-3 pb-2 border-b">
        <div className="flex items-center gap-2">
          <LineChart className="w-8 h-8 text-primary" />
          <h1 className="text-3xl font-bold tracking-tight">Economic Analysis</h1>
        </div>
        <nav className="flex items-center gap-2 ml-auto text-sm">
          <Button variant="ghost" size="sm" asChild className="text-muted-foreground hover:text-foreground">
            <Link href="/dashboard" className="flex items-center gap-1">
              <Home className="w-4 h-4" />
              Dashboard
            </Link>
          </Button>
          <ArrowRight className="w-4 h-4 text-muted-foreground" />
          <span className="text-foreground font-medium">Analysis</span>
        </nav>
      </div>
      
      <Card className="p-6 shadow-lg bg-gradient-to-b from-background to-muted/10">
        {children}
      </Card>
    </div>
  );
}

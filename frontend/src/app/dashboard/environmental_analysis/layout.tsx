import React from 'react';
import { Leaf } from 'lucide-react';
import { Card } from "@/components/ui/card";
import { TooltipProvider } from "@/components/ui/tooltip";

interface EnvironmentalAnalysisLayoutProps {
  children: React.ReactNode;
}

export default function EnvironmentalAnalysisLayout({ children }: EnvironmentalAnalysisLayoutProps) {
  return (
    <div className="container mx-auto py-8 space-y-6 animate-in fade-in duration-500">
      <Card className="p-6 shadow-lg bg-gradient-to-b from-background to-muted/10">
        <TooltipProvider>
          {children}
        </TooltipProvider>
      </Card>
    </div>
  );
}

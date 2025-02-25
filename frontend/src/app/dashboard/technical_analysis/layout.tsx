import React from 'react';
import { Card } from "@/components/ui/card";
import { Activity, ArrowRight, Home, Microscope, Gauge, Atom } from 'lucide-react';
import Link from 'next/link';
import { Button } from "@/components/ui/button";
import { Separator } from "@/components/ui/separator";

interface TechnicalAnalysisLayoutProps {
  children: React.ReactNode;
}

export default function TechnicalAnalysisLayout({ children }: TechnicalAnalysisLayoutProps) {
  const features = [
    {
      icon: <Microscope className="w-4 h-4" />,
      label: "Protein Recovery",
      description: "Analysis of protein extraction and concentration"
    },
    {
      icon: <Gauge className="w-4 h-4" />,
      label: "Process Efficiency",
      description: "Separation and processing performance metrics"
    },
    {
      icon: <Atom className="w-4 h-4" />,
      label: "Particle Analysis",
      description: "Size distribution and quality assessment"
    }
  ];

  return (
    <div className="container mx-auto py-8 space-y-6 animate-in fade-in duration-500">
      <div className="flex items-center gap-3 pb-2 border-b">
        <div className="flex items-center gap-2">
          <Activity className="w-8 h-8 text-blue-500" />
          <h1 className="text-3xl font-bold tracking-tight">Technical Analysis</h1>
        </div>
        <nav className="flex items-center gap-2 ml-auto text-sm">
          <Button variant="ghost" size="sm" asChild className="text-muted-foreground hover:text-foreground">
            <Link href="/dashboard" className="flex items-center gap-1">
              <Home className="w-4 h-4" />
              Dashboard
            </Link>
          </Button>
          <ArrowRight className="w-4 h-4 text-muted-foreground" />
          <span className="text-foreground font-medium">Technical Analysis</span>
        </nav>
      </div>

      <div className="grid gap-6 md:grid-cols-3 mb-6">
        {features.map((feature) => (
          <Card key={feature.label} className="p-4">
            <div className="flex items-start gap-3">
              <div className="p-2 rounded-md bg-blue-500/10 text-blue-500">
                {feature.icon}
              </div>
              <div>
                <h3 className="font-medium">{feature.label}</h3>
                <p className="text-sm text-muted-foreground">
                  {feature.description}
                </p>
              </div>
            </div>
          </Card>
        ))}
      </div>

      <Separator className="my-6" />
      
      <Card className="p-6 shadow-lg bg-gradient-to-b from-background to-muted/10">
        {children}
      </Card>

      <footer className="mt-8 text-center text-sm text-muted-foreground">
        <p>
          Technical analysis tools for pea protein processing optimization.
          All calculations follow industry standards and best practices.
        </p>
      </footer>
    </div>
  );
}

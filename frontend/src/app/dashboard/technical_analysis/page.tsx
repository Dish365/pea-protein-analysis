"use client";

import React from 'react';
import { Card, CardContent } from "@/components/ui/card";
import { Activity, Construction, ArrowRight } from 'lucide-react';
import { Button } from "@/components/ui/button";
import Link from 'next/link';

export default function TechnicalAnalysisPage() {
  return (
    <div className="flex flex-col items-center justify-center py-12 text-center space-y-6">
      <div className="relative">
        <div className="absolute inset-0 animate-spin-slow">
          <Activity className="w-24 h-24 text-blue-500/20" />
        </div>
        <Construction className="w-24 h-24 text-blue-500 relative" />
      </div>
      
      <div className="space-y-2 max-w-[500px]">
        <h2 className="text-2xl font-bold tracking-tight">
          Technical Analysis Coming Soon
        </h2>
        <p className="text-muted-foreground">
          We're working hard to bring you comprehensive technical analysis tools for process optimization, 
          efficiency metrics, and performance indicators. Stay tuned for updates!
        </p>
      </div>

      <div className="flex flex-col items-center gap-4 mt-4">
        <div className="text-sm text-muted-foreground">
          Expected features:
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm max-w-[600px]">
          <Card className="bg-muted/50">
            <CardContent className="p-4 flex items-start gap-3">
              <Activity className="w-5 h-5 text-blue-500 mt-0.5" />
              <div className="text-left">
                <p className="font-medium">Process Efficiency Analysis</p>
                <p className="text-muted-foreground">Detailed metrics and optimization recommendations</p>
              </div>
            </CardContent>
          </Card>
          <Card className="bg-muted/50">
            <CardContent className="p-4 flex items-start gap-3">
              <Activity className="w-5 h-5 text-blue-500 mt-0.5" />
              <div className="text-left">
                <p className="font-medium">Performance Monitoring</p>
                <p className="text-muted-foreground">Real-time tracking and analysis tools</p>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>

      <Button asChild className="mt-8">
        <Link href="/dashboard" className="flex items-center gap-2">
          Return to Dashboard
          <ArrowRight className="w-4 h-4" />
        </Link>
      </Button>
    </div>
  );
}

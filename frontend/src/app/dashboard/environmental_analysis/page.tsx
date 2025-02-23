"use client";

import React from 'react';
import { Card, CardContent } from "@/components/ui/card";
import { Leaf, Construction, ArrowRight, Droplets, Wind } from 'lucide-react';
import { Button } from "@/components/ui/button";
import Link from 'next/link';

export default function EnvironmentalAnalysisPage() {
  return (
    <div className="flex flex-col items-center justify-center py-12 text-center space-y-6">
      <div className="relative">
        <div className="absolute inset-0 animate-spin-slow">
          <Leaf className="w-24 h-24 text-emerald-500/20" />
        </div>
        <Construction className="w-24 h-24 text-emerald-500 relative" />
      </div>
      
      <div className="space-y-2 max-w-[500px]">
        <h2 className="text-2xl font-bold tracking-tight">
          Environmental Analysis Coming Soon
        </h2>
        <p className="text-muted-foreground">
          We're developing comprehensive environmental impact assessment tools to help you analyze 
          and optimize your process's sustainability metrics. Stay tuned for our upcoming release!
        </p>
      </div>

      <div className="flex flex-col items-center gap-4 mt-4">
        <div className="text-sm text-muted-foreground">
          Upcoming features:
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm max-w-[600px]">
          <Card className="bg-muted/50">
            <CardContent className="p-4 flex items-start gap-3">
              <Droplets className="w-5 h-5 text-emerald-500 mt-0.5" />
              <div className="text-left">
                <p className="font-medium">Water Impact Analysis</p>
                <p className="text-muted-foreground">Water usage and efficiency metrics</p>
              </div>
            </CardContent>
          </Card>
          <Card className="bg-muted/50">
            <CardContent className="p-4 flex items-start gap-3">
              <Wind className="w-5 h-5 text-emerald-500 mt-0.5" />
              <div className="text-left">
                <p className="font-medium">Carbon Footprint Assessment</p>
                <p className="text-muted-foreground">Emissions tracking and reduction strategies</p>
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

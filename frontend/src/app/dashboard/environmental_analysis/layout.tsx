import React from 'react';
import { Card } from "@/components/ui/card";
import { Leaf, ArrowRight, Home, CloudRain, Droplets, Factory, Info } from 'lucide-react';
import Link from 'next/link';
import { Button } from "@/components/ui/button";
import { Separator } from "@/components/ui/separator";
import { MotionDiv, MotionFooter } from "@/components/motion";
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from "@/components/ui/tooltip";

interface EnvironmentalAnalysisLayoutProps {
  children: React.ReactNode;
}

export default function EnvironmentalAnalysisLayout({ children }: EnvironmentalAnalysisLayoutProps) {
  const features = [
    {
      icon: <CloudRain className="w-5 h-5" />,
      label: "Global Warming Impact",
      description: "CO2 emissions and GWP analysis",
      color: "bg-red-500/10 text-red-500",
      tooltip: "Global Warming Potential (GWP) measured in kg CO2 equivalent, including electricity, water, and transport contributions"
    },
    {
      icon: <Droplets className="w-5 h-5" />,
      label: "Water Consumption",
      description: "Process water usage and efficiency",
      color: "bg-blue-500/10 text-blue-500",
      tooltip: "Total water consumption across tempering, cleaning, and cooling processes measured in kg water"
    },
    {
      icon: <Factory className="w-5 h-5" />,
      label: "Resource Depletion",
      description: "Fossil resource consumption",
      color: "bg-amber-500/10 text-amber-500",
      tooltip: "Fossil Resource Scarcity (FRS) measured in kg oil equivalent, including electricity, thermal, and mechanical processing"
    }
  ];

  return (
    <TooltipProvider>
      <div className="container mx-auto py-8 space-y-6">
        <MotionDiv 
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="flex items-center gap-3 pb-2 border-b"
        >
          <div className="flex items-center gap-2">
            <div className="p-2 rounded-lg bg-emerald-500/10">
              <Leaf className="w-8 h-8 text-emerald-500" />
            </div>
            <div>
              <h1 className="text-3xl font-bold tracking-tight">Environmental Analysis</h1>
              <p className="text-sm text-muted-foreground">
                Process impact assessment and sustainability metrics
              </p>
            </div>
          </div>
          <nav className="flex items-center gap-2 ml-auto text-sm">
            <Button variant="ghost" size="sm" asChild className="text-muted-foreground hover:text-foreground">
              <Link href="/dashboard" className="flex items-center gap-1">
                <Home className="w-4 h-4" />
                Dashboard
              </Link>
            </Button>
            <ArrowRight className="w-4 h-4 text-muted-foreground" />
            <span className="text-foreground font-medium">Environmental Analysis</span>
          </nav>
        </MotionDiv>

        <MotionDiv 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.2 }}
          className="grid gap-6 md:grid-cols-3 mb-6"
        >
          {features.map((feature, index) => (
            <MotionDiv
              key={feature.label}
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.3, delay: index * 0.1 }}
            >
              <Card className="p-4 hover:shadow-lg transition-shadow duration-300 cursor-default group">
                <div className="flex items-start gap-3">
                  <div className={`p-2 rounded-md ${feature.color} transition-colors duration-300 group-hover:bg-opacity-20`}>
                    {feature.icon}
                  </div>
                  <div className="flex-1">
                    <div className="flex items-center gap-2">
                      <h3 className="font-medium">{feature.label}</h3>
                      <Tooltip>
                        <TooltipTrigger asChild>
                          <Info className="w-4 h-4 text-muted-foreground/50 hover:text-muted-foreground cursor-help" />
                        </TooltipTrigger>
                        <TooltipContent>
                          <p className="max-w-[200px]">{feature.tooltip}</p>
                        </TooltipContent>
                      </Tooltip>
                    </div>
                    <p className="text-sm text-muted-foreground">
                      {feature.description}
                    </p>
                  </div>
                </div>
              </Card>
            </MotionDiv>
          ))}
        </MotionDiv>

        <Separator className="my-6" />
        
        <MotionDiv
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.4 }}
        >
          <Card className="p-6 shadow-lg bg-gradient-to-b from-background to-muted/10 border-none">
            {children}
          </Card>
        </MotionDiv>

        <MotionFooter 
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.5, delay: 0.6 }}
          className="mt-8 text-center space-y-2"
        >
          <p className="text-sm text-muted-foreground">
            Environmental impact assessment tools for pea protein processing optimization.
          </p>
          <p className="text-xs text-muted-foreground/60">
            Analysis based on RF processing parameters and economic allocation methods.
          </p>
        </MotionFooter>
      </div>
    </TooltipProvider>
  );
}

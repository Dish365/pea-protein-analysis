"use client";

import React from 'react';
import { 
  Activity, 
  DollarSign, 
  Leaf, 
  ArrowRight, 
  CircleDollarSign,
  Target,
  Droplets,
  TrendingUp,
  LineChart,
  Wind,
  Scale,
  Package,
  ArrowUpRight
} from 'lucide-react';
import { Button } from "@/components/ui/button";
import Link from "next/link";
import { Card } from "@/components/ui/card";
import { MotionDiv } from "@/components/motion";
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip";

const features = [
  {
    title: "Economic Analysis",
    description: "Comprehensive financial assessment of your pea protein extraction process",
    icon: DollarSign,
    color: "text-green-500",
    bgGradient: "from-green-500/5 via-transparent to-transparent",
    borderColor: "group-hover:border-green-500/50",
    subFeatures: [
      { icon: CircleDollarSign, label: "Cost Breakdown Analysis" },
      { icon: TrendingUp, label: "Profitability Metrics" },
      { icon: LineChart, label: "Sensitivity Analysis" }
    ]
  },
  {
    title: "Technical Analysis",
    description: "In-depth evaluation of process efficiency and performance metrics",
    icon: Activity,
    color: "text-blue-500",
    bgGradient: "from-blue-500/5 via-transparent to-transparent",
    borderColor: "group-hover:border-blue-500/50",
    subFeatures: [
      { icon: Target, label: "Process Efficiency" },
      { icon: Activity, label: "Performance Monitoring" },
      { icon: Package, label: "Resource Optimization" }
    ]
  },
  {
    title: "Environmental Analysis",
    description: "Comprehensive assessment of environmental impact and sustainability",
    icon: Leaf,
    color: "text-emerald-500",
    bgGradient: "from-emerald-500/5 via-transparent to-transparent",
    borderColor: "group-hover:border-emerald-500/50",
    subFeatures: [
      { icon: Droplets, label: "Water Impact Analysis" },
      { icon: Wind, label: "Carbon Footprint" },
      { icon: Scale, label: "Resource Efficiency" }
    ]
  }
];

const benefits = [
  {
    title: "Data-Driven Insights",
    description: "Make informed decisions based on comprehensive analysis and real-time data",
    gradient: "from-blue-500/20 via-transparent"
  },
  {
    title: "Process Optimization",
    description: "Identify opportunities to improve efficiency and reduce operational costs",
    gradient: "from-green-500/20 via-transparent"
  },
  {
    title: "Sustainability Focus",
    description: "Track and improve your environmental impact metrics with detailed analytics",
    gradient: "from-emerald-500/20 via-transparent"
  },
  {
    title: "Easy Integration",
    description: "Seamlessly integrate with your existing production processes and workflows",
    gradient: "from-purple-500/20 via-transparent"
  }
] as const;

export default function Home() {
  return (
    <div className="flex flex-col min-h-screen">
      {/* Hero Section */}
      <section className="relative flex-1 flex flex-col items-center justify-center px-4 sm:px-6 lg:px-8 py-24 overflow-hidden">
        {/* Animated Background Patterns */}
        <div className="absolute inset-0">
          <div className="absolute inset-0 bg-grid-small-black/[0.02] -z-10" />
          <div className="absolute inset-0 bg-gradient-to-b from-background/80 via-background to-background/80 backdrop-blur-[2px]" />
          
          {/* Animated Gradient Orbs */}
          <MotionDiv
            className="absolute top-1/4 -right-32 w-[500px] h-[500px] bg-gradient-to-br from-blue-500/20 to-purple-500/20 rounded-full blur-3xl"
            animate={{
              scale: [1, 1.2, 1],
              x: [0, 50, 0],
              y: [0, 30, 0],
              opacity: [0.3, 0.5, 0.3],
            }}
            transition={{
              duration: 15,
              repeat: Infinity,
              ease: "easeInOut"
            }}
          />
          <MotionDiv
            className="absolute -bottom-32 -left-32 w-[500px] h-[500px] bg-gradient-to-tr from-emerald-500/20 to-cyan-500/20 rounded-full blur-3xl"
            animate={{
              scale: [1.2, 1, 1.2],
              x: [0, -50, 0],
              y: [0, -30, 0],
              opacity: [0.3, 0.5, 0.3],
            }}
            transition={{
              duration: 15,
              repeat: Infinity,
              ease: "easeInOut",
              delay: 2
            }}
          />
          <MotionDiv
            className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] bg-gradient-to-r from-primary/20 via-purple-500/20 to-blue-500/20 rounded-full blur-3xl opacity-50"
            animate={{
              scale: [1, 1.1, 1],
              rotate: [0, 360],
              opacity: [0.3, 0.4, 0.3],
            }}
            transition={{
              duration: 20,
              repeat: Infinity,
              ease: "linear"
            }}
          />
        </div>

        {/* Hero Content */}
        <MotionDiv 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className="relative max-w-5xl mx-auto text-center space-y-8"
        >
          <div className="space-y-6">
            <div className="relative inline-block">
              <MotionDiv
                className="absolute inset-0 bg-gradient-to-r from-primary/50 via-purple-500/50 to-blue-500/50 blur-3xl opacity-30"
                animate={{
                  scale: [1, 1.1, 1],
                  opacity: [0.3, 0.4, 0.3],
                }}
                transition={{
                  duration: 4,
                  repeat: Infinity,
                  ease: "easeInOut"
                }}
              />
              <h1 className="relative text-4xl sm:text-5xl lg:text-6xl font-bold tracking-tight">
                <span className="bg-gradient-to-r from-primary via-purple-500 to-blue-500 bg-clip-text text-transparent">
                  Pea Protein Extraction
                </span>
                <br />
                <span className="bg-gradient-to-r from-blue-500 via-primary to-emerald-500 bg-clip-text text-transparent">
                  Analysis
                </span>
              </h1>
            </div>
            <p className="text-xl text-muted-foreground max-w-3xl mx-auto backdrop-blur-sm bg-background/30 rounded-full px-4 py-2">
              Optimize your pea protein extraction process with comprehensive technical, 
              economic, and environmental analysis tools
            </p>
          </div>
          
          <div className="flex flex-wrap items-center justify-center gap-4">
            <TooltipProvider>
              <Tooltip>
                <TooltipTrigger asChild>
                  <Button 
                    asChild 
                    size="lg" 
                    className="gap-2 relative overflow-hidden group bg-gradient-to-r from-primary to-purple-500 hover:from-primary/90 hover:to-purple-500/90"
                  >
                    <Link href="/dashboard">
                      Get Started
                      <ArrowRight className="h-4 w-4 transition-transform group-hover:translate-x-1" />
                      <MotionDiv
                        className="absolute inset-0 bg-primary/10"
                        initial={{ scale: 0, opacity: 0 }}
                        whileHover={{ scale: 1, opacity: 1 }}
                        transition={{ duration: 0.2 }}
                      />
                    </Link>
                  </Button>
                </TooltipTrigger>
                <TooltipContent>
                  <p>Start optimizing your process</p>
                </TooltipContent>
              </Tooltip>

              <Tooltip>
                <TooltipTrigger asChild>
                  <Button 
                    asChild 
                    variant="outline" 
                    size="lg" 
                    className="relative overflow-hidden group backdrop-blur-sm bg-background/50"
                  >
                    <Link href="/documentation">
                      Learn More
                      <MotionDiv
                        className="absolute inset-0 bg-muted/50"
                        initial={{ scale: 0, opacity: 0 }}
                        whileHover={{ scale: 1, opacity: 1 }}
                        transition={{ duration: 0.2 }}
                      />
                    </Link>
                  </Button>
                </TooltipTrigger>
                <TooltipContent>
                  <p>Explore our documentation</p>
                </TooltipContent>
              </Tooltip>
            </TooltipProvider>
          </div>
        </MotionDiv>
      </section>

      {/* Features Section */}
      <section className="relative py-24 px-4 sm:px-6 lg:px-8 overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-b from-background via-background to-muted/20" />
        <div className="relative max-w-7xl mx-auto">
          <MotionDiv 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="text-center space-y-4 mb-16"
          >
            <h2 className="text-3xl font-bold bg-gradient-to-r from-foreground to-foreground/70 bg-clip-text text-transparent">
              Comprehensive Analysis Suite
            </h2>
            <p className="text-lg text-muted-foreground max-w-3xl mx-auto">
              Our platform provides powerful tools for analyzing every aspect of your pea protein extraction process
            </p>
          </MotionDiv>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {features.map((feature, index) => (
              <MotionDiv
                key={feature.title}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: index * 0.1 }}
              >
                <Card 
                  className={`
                    group relative overflow-hidden border 
                    transition-all duration-300 hover:shadow-lg
                    bg-gradient-to-br ${feature.bgGradient}
                    border ${feature.borderColor}
                  `}
                >
                  <div className="p-6 space-y-4">
                    <div className="space-y-2">
                      <div className="flex items-center gap-2">
                        <MotionDiv
                          whileHover={{ rotate: 5, scale: 1.1 }}
                          transition={{ type: "spring", stiffness: 400, damping: 10 }}
                          className={`p-2 rounded-lg bg-gradient-to-br from-${feature.color}/20 to-${feature.color}/10`}
                        >
                          <feature.icon className={`h-6 w-6 ${feature.color}`} />
                        </MotionDiv>
                        <h3 className="text-xl font-semibold">{feature.title}</h3>
                      </div>
                      <p className="text-sm text-muted-foreground">
                        {feature.description}
                      </p>
                    </div>

                    <div className="space-y-2 pt-2">
                      {feature.subFeatures.map((subFeature, subIndex) => (
                        <MotionDiv 
                          key={subFeature.label}
                          initial={{ opacity: 0, x: -10 }}
                          animate={{ opacity: 1, x: 0 }}
                          transition={{ duration: 0.3, delay: (index * 0.1) + (subIndex * 0.1) }}
                          whileHover={{ x: 4 }}
                          className="flex items-center gap-2 text-sm group/item"
                        >
                          <subFeature.icon className={`h-4 w-4 ${feature.color} transition-transform group-hover/item:scale-110`} />
                          <span>{subFeature.label}</span>
                        </MotionDiv>
                      ))}
                    </div>
                  </div>
                </Card>
              </MotionDiv>
            ))}
          </div>
        </div>
      </section>

      {/* Benefits Section */}
      <section className="relative py-24 px-4 sm:px-6 lg:px-8 bg-muted/50">
        <div className="absolute inset-0 bg-gradient-to-b from-muted/50 to-background/50" />
        <MotionDiv 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="relative max-w-7xl mx-auto text-center"
        >
          <h2 className="text-3xl font-bold mb-16 bg-gradient-to-r from-foreground to-foreground/70 bg-clip-text text-transparent">
            Why Choose Our Platform?
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {benefits.map((benefit, index) => (
              <MotionDiv
                key={benefit.title}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: index * 0.1 }}
              >
                <Card 
                  className={`
                    relative overflow-hidden
                    transition-all duration-300
                    hover:shadow-lg hover:-translate-y-1
                    bg-gradient-to-br ${benefit.gradient}
                  `}
                >
                  <div className="p-6">
                    <h3 className="text-lg font-semibold mb-2">
                      {benefit.title}
                    </h3>
                    <p className="text-sm text-muted-foreground">
                      {benefit.description}
                    </p>
                  </div>
                </Card>
              </MotionDiv>
            ))}
          </div>
        </MotionDiv>
      </section>

      {/* CTA Section */}
      <section className="relative py-24 px-4 sm:px-6 lg:px-8">
        <div className="absolute inset-0 bg-gradient-to-b from-primary/20 via-primary/10 to-background" />
        <MotionDiv 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="relative max-w-4xl mx-auto text-center space-y-8"
        >
          <div className="space-y-4">
            <h2 className="text-3xl font-bold bg-gradient-to-r from-foreground to-foreground/70 bg-clip-text text-transparent">
              Ready to Optimize Your Process?
            </h2>
            <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
              Start analyzing your pea protein extraction process today with our comprehensive suite of tools
            </p>
          </div>
          
          <div className="flex flex-wrap items-center justify-center gap-4">
            <Button 
              asChild 
              size="lg"
              className="gap-2 group"
            >
              <Link href="/dashboard">
                Get Started
                <ArrowUpRight className="h-4 w-4 transition-transform group-hover:translate-x-1 group-hover:-translate-y-1" />
              </Link>
            </Button>
            <Button 
              asChild 
              variant="outline" 
              size="lg"
              className="group"
            >
              <Link href="/contact">
                Contact Us
                <ArrowRight className="h-4 w-4 ml-2 transition-transform group-hover:translate-x-1" />
              </Link>
            </Button>
          </div>
        </MotionDiv>
      </section>
    </div>
  );
}

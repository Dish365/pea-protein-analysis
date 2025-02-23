"use client";

import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";
import Link from "next/link";
import {
  Book,
  DollarSign,
  Activity,
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
  FileText,
  Settings,
  HelpCircle
} from 'lucide-react';

const documentationSections = [
  {
    id: "getting-started",
    title: "Getting Started",
    icon: Book,
    content: [
      {
        title: "Platform Overview",
        description: "Learn about the core features and capabilities of our platform",
        link: "#platform-overview"
      },
      {
        title: "Quick Start Guide",
        description: "Get up and running with your first analysis in minutes",
        link: "#quick-start"
      },
      {
        title: "System Requirements",
        description: "Technical requirements and recommended specifications",
        link: "#requirements"
      }
    ]
  },
  {
    id: "analysis-guides",
    title: "Analysis Guides",
    icon: FileText,
    content: [
      {
        title: "Economic Analysis",
        description: "Comprehensive guide to financial assessment tools",
        icon: DollarSign,
        color: "text-green-500",
        features: [
          "Cost breakdown analysis methodology",
          "Profitability metrics calculation",
          "Sensitivity analysis tools"
        ]
      },
      {
        title: "Technical Analysis",
        description: "Guide to process efficiency and performance metrics",
        icon: Activity,
        color: "text-blue-500",
        features: [
          "Process efficiency evaluation",
          "Performance monitoring tools",
          "Resource optimization techniques"
        ]
      },
      {
        title: "Environmental Analysis",
        description: "Understanding environmental impact assessment",
        icon: Leaf,
        color: "text-emerald-500",
        features: [
          "Water impact analysis methods",
          "Carbon footprint calculation",
          "Resource efficiency metrics"
        ]
      }
    ]
  },
  {
    id: "technical-docs",
    title: "Technical Documentation",
    icon: Settings,
    content: [
      {
        title: "API Reference",
        description: "Complete API documentation for integration",
        link: "#api-reference"
      },
      {
        title: "Data Models",
        description: "Understanding data structures and relationships",
        link: "#data-models"
      },
      {
        title: "Integration Guide",
        description: "Steps for integrating with existing systems",
        link: "#integration"
      }
    ]
  }
];

export default function DocumentationPage() {
  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b bg-card/50 backdrop-blur-sm sticky top-0 z-50">
        <div className="container mx-auto py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Book className="h-6 w-6" />
              <h1 className="text-2xl font-bold">Documentation</h1>
            </div>
            <Button asChild variant="outline" size="sm">
              <Link href="/dashboard" className="gap-2">
                Go to Dashboard
                <ArrowRight className="h-4 w-4" />
              </Link>
            </Button>
          </div>
        </div>
      </header>

      <main className="container mx-auto py-8 space-y-12">
        {/* Introduction */}
        <section className="max-w-4xl mx-auto text-center space-y-4">
          <h1 className="text-4xl font-bold tracking-tight">
            Platform Documentation
          </h1>
          <p className="text-lg text-muted-foreground">
            Comprehensive guides and documentation for the PEA Protein Analysis Platform
          </p>
        </section>

        {/* Documentation Sections */}
        <Tabs defaultValue="getting-started" className="space-y-8">
          <TabsList className="w-full justify-start border-b rounded-none p-0 h-auto gap-4">
            {documentationSections.map((section) => (
              <TabsTrigger
                key={section.id}
                value={section.id}
                className="data-[state=active]:bg-background border-b-2 border-transparent data-[state=active]:border-primary rounded-none"
              >
                <div className="flex items-center gap-2 py-2">
                  <section.icon className="h-4 w-4" />
                  {section.title}
                </div>
              </TabsTrigger>
            ))}
          </TabsList>

          {documentationSections.map((section) => (
            <TabsContent
              key={section.id}
              value={section.id}
              className="space-y-8 animate-in fade-in-50 duration-500"
            >
              <div className="grid gap-6">
                {section.content.map((item, index) => (
                  <Card key={item.title} className="overflow-hidden">
                    <CardHeader>
                      <CardTitle className="flex items-center gap-2">
                        {'icon' in item && <item.icon className={cn("h-5 w-5", item.color)} />}
                        {item.title}
                      </CardTitle>
                    </CardHeader>
                    <CardContent className="space-y-4">
                      <p className="text-muted-foreground">{item.description}</p>
                      {'features' in item && (
                        <ul className="space-y-2 ml-6 list-disc text-sm text-muted-foreground">
                          {item.features.map((feature: string) => (
                            <li key={feature}>{feature}</li>
                          ))}
                        </ul>
                      )}
                      {'link' in item && (
                        <Button variant="outline" asChild className="gap-2">
                          <Link href={item.link}>
                            Learn More
                            <ArrowRight className="h-4 w-4" />
                          </Link>
                        </Button>
                      )}
                    </CardContent>
                  </Card>
                ))}
              </div>
            </TabsContent>
          ))}
        </Tabs>

        {/* Help Section */}
        <section className="border-t pt-12">
          <div className="max-w-4xl mx-auto text-center space-y-6">
            <div className="flex justify-center">
              <div className="inline-flex items-center gap-2 text-primary px-4 py-2 rounded-full bg-primary/10">
                <HelpCircle className="h-4 w-4" />
                <span className="font-medium">Need Help?</span>
              </div>
            </div>
            <h2 className="text-2xl font-bold">Can't find what you're looking for?</h2>
            <p className="text-muted-foreground">
              Our support team is here to help. Contact us for personalized assistance.
            </p>
            <Button asChild size="lg">
              <Link href="/contact">Contact Support</Link>
            </Button>
          </div>
        </section>
      </main>
    </div>
  );
} 
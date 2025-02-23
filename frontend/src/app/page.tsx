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
  Package
} from 'lucide-react';
import { Button } from "@/components/ui/button";
import Link from "next/link";
import { Card } from "@/components/ui/card";

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
        <div className="absolute inset-0 bg-gradient-to-b from-background to-background/80 backdrop-blur-sm" />
        <div className="relative max-w-5xl mx-auto text-center space-y-8">
          <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-1000">
            <h1 className="text-4xl sm:text-5xl lg:text-6xl font-bold tracking-tight">
              Pea Protein Process Analysis Platform
            </h1>
            <p className="text-xl text-muted-foreground max-w-3xl mx-auto">
              Optimize your pea protein extraction process with comprehensive technical, 
              economic, and environmental analysis tools
            </p>
          </div>
          
          <div className="flex flex-wrap items-center justify-center gap-4 animate-in fade-in slide-in-from-bottom-4 duration-1000 delay-200">
            <Button asChild size="lg" className="gap-2">
              <Link href="/dashboard">
                Get Started
                <ArrowRight className="h-4 w-4" />
              </Link>
            </Button>
            <Button asChild variant="outline" size="lg">
              <Link href="/documentation">
                Learn More
              </Link>
            </Button>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-24 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <div className="text-center space-y-4 mb-16">
            <h2 className="text-3xl font-bold">Comprehensive Analysis Suite</h2>
            <p className="text-lg text-muted-foreground max-w-3xl mx-auto">
              Our platform provides powerful tools for analyzing every aspect of your pea protein extraction process
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {features.map((feature, index) => (
              <Card 
                key={feature.title}
                className={`
                  group relative overflow-hidden border 
                  transition-all duration-300 hover:shadow-lg
                  animate-in fade-in slide-in-from-bottom-4
                  bg-gradient-to-br ${feature.bgGradient}
                  border ${feature.borderColor}
                `}
                style={{ animationDelay: `${index * 150}ms` }}
              >
                <div className="p-6 space-y-4">
                  <div className="space-y-2">
                    <div className="flex items-center gap-2">
                      <feature.icon className={`h-6 w-6 ${feature.color}`} />
                      <h3 className="text-xl font-semibold">{feature.title}</h3>
                    </div>
                    <p className="text-sm text-muted-foreground">
                      {feature.description}
                    </p>
                  </div>

                  <div className="space-y-2 pt-2">
                    {feature.subFeatures.map((subFeature, subIndex) => (
                      <div 
                        key={subFeature.label}
                        className={`
                          flex items-center gap-2 text-sm
                          animate-in fade-in slide-in-from-bottom-2
                        `}
                        style={{ animationDelay: `${(index * 150) + (subIndex * 100)}ms` }}
                      >
                        <subFeature.icon className={`h-4 w-4 ${feature.color}`} />
                        <span>{subFeature.label}</span>
                      </div>
                    ))}
                  </div>
                </div>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Benefits Section */}
      <section className="py-24 px-4 sm:px-6 lg:px-8 bg-muted/50">
        <div className="max-w-7xl mx-auto text-center">
          <h2 className="text-3xl font-bold mb-16">
            Why Choose Our Platform?
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {benefits.map((benefit, index) => (
              <Card 
                key={benefit.title}
                className={`
                  relative overflow-hidden
                  transition-all duration-300
                  hover:shadow-lg hover:scale-[1.02]
                  animate-in fade-in slide-in-from-bottom-4
                  bg-gradient-to-br ${benefit.gradient}
                `}
                style={{ animationDelay: `${index * 150}ms` }}
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
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-24 px-4 sm:px-6 lg:px-8 bg-primary text-primary-foreground">
        <div className="max-w-4xl mx-auto text-center space-y-8">
          <div className="space-y-4">
            <h2 className="text-3xl font-bold">
              Ready to Optimize Your Process?
            </h2>
            <p className="text-lg opacity-90 max-w-2xl mx-auto">
              Start analyzing your pea protein extraction process today with our comprehensive suite of tools
            </p>
          </div>
          
          <div className="flex flex-wrap items-center justify-center gap-4">
            <Button 
              asChild 
              variant="secondary" 
              size="lg"
              className="gap-2"
            >
              <Link href="/dashboard">
                Get Started
                <ArrowRight className="h-4 w-4" />
              </Link>
            </Button>
            <Button 
              asChild 
              variant="outline" 
              size="lg"
              className="bg-transparent text-primary-foreground hover:bg-primary-foreground/10"
            >
              <Link href="/contact">
                Contact Us
              </Link>
            </Button>
          </div>
        </div>
      </section>
    </div>
  );
}

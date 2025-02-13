import React from 'react';
import { Activity, DollarSign, Leaf } from 'lucide-react';
import { CTAButtons } from '@/components/landing/CTAButtons';

const benefits = [
  {
    title: "Data-Driven Insights",
    description: "Make informed decisions based on comprehensive analysis and real-time data"
  },
  {
    title: "Process Optimization",
    description: "Identify opportunities to improve efficiency and reduce costs"
  },
  {
    title: "Sustainability Focus",
    description: "Track and improve your environmental impact metrics"
  },
  {
    title: "Easy Integration",
    description: "Seamlessly integrate with your existing production processes"
  }
] as const;

export default function Home() {
  return (
    <div className="flex flex-col min-h-screen">
      {/* Hero Section */}
      <section className="flex-1 flex flex-col items-center justify-center px-4 sm:px-6 lg:px-8 py-12 bg-gradient-to-b from-white to-gray-50">
        <div className="max-w-4xl mx-auto text-center">
          <h1 className="text-4xl sm:text-5xl lg:text-6xl font-bold text-gray-900 mb-6">
            Pea Protein Process Analysis Platform
          </h1>
          <p className="text-xl text-gray-600 mb-8">
            Optimize your pea protein extraction process with comprehensive technical, economic, and environmental analysis
          </p>
          <CTAButtons />
        </div>
      </section>

      {/* Features Section */}
      <section className="py-16 px-4 sm:px-6 lg:px-8 bg-white">
        <div className="max-w-7xl mx-auto">
          <h2 className="text-3xl font-bold text-center text-gray-900 mb-12">
            Comprehensive Analysis Suite
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="border-2 rounded-lg p-6 hover:border-primary/50 transition-colors">
              <div className="flex items-center gap-2 font-semibold mb-4">
                <Activity className="h-5 w-5 text-blue-600" />
                Technical Analysis
              </div>
              <p className="text-gray-600">
                Evaluate process efficiency, yield optimization, and quality parameters for your pea protein extraction
              </p>
            </div>

            <div className="border-2 rounded-lg p-6 hover:border-primary/50 transition-colors">
              <div className="flex items-center gap-2 font-semibold mb-4">
                <DollarSign className="h-5 w-5 text-green-600" />
                Economic Analysis
              </div>
              <p className="text-gray-600">
                Calculate ROI, operating costs, and profitability metrics for your production process
              </p>
            </div>

            <div className="border-2 rounded-lg p-6 hover:border-primary/50 transition-colors">
              <div className="flex items-center gap-2 font-semibold mb-4">
                <Leaf className="h-5 w-5 text-purple-600" />
                Environmental Analysis
              </div>
              <p className="text-gray-600">
                Assess environmental impact, resource efficiency, and sustainability metrics
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Benefits Section */}
      <section className="py-16 px-4 sm:px-6 lg:px-8 bg-gray-50">
        <div className="max-w-7xl mx-auto text-center">
          <h2 className="text-3xl font-bold text-gray-900 mb-8">
            Why Choose Our Platform?
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {benefits.map((benefit, index) => (
              <div key={index} className="p-6 bg-white rounded-lg shadow-sm">
                <h3 className="text-lg font-semibold text-gray-900 mb-2">
                  {benefit.title}
                </h3>
                <p className="text-gray-600">
                  {benefit.description}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-16 px-4 sm:px-6 lg:px-8 bg-primary text-primary-foreground">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-3xl font-bold mb-4">
            Ready to Optimize Your Process?
          </h2>
          <p className="text-lg mb-8 opacity-90">
            Start analyzing your pea protein extraction process today
          </p>
          <CTAButtons variant="secondary" />
        </div>
      </section>
    </div>
  );
}

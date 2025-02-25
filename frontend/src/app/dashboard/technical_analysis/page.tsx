"use client";

import React, { useState } from 'react';
import TechnicalInputForm from "@/components/forms/TechnicalInputForm";
import { TechnicalAnalysisView } from "@/features/analysis/technical/components/TechnicalAnalysisView";
import { TechnicalParameters, TechnicalResults } from "@/types/technical";
import { API_CONFIG, API_ENDPOINTS } from "@/config/api";
import { useToast } from "@/components/ui/use-toast";
import { Card } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";

export default function TechnicalAnalysisPage() {
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [results, setResults] = useState<TechnicalResults | undefined>();
  const [error, setError] = useState<string | undefined>();
  const [activeTab, setActiveTab] = useState<string>("input");
  const { toast } = useToast();

  const handleAnalysis = async (parameters: TechnicalParameters) => {
    setIsAnalyzing(true);
    setError(undefined);
    
    try {
      console.log('Sending analysis request with parameters:', parameters);

      const response = await fetch(API_ENDPOINTS.protein.completeAnalysis, {
        method: 'POST',
        headers: API_CONFIG.headers,
        body: JSON.stringify({
          recovery_input: {
            input_mass: parameters.input_mass,
            output_mass: parameters.output_mass,
            initial_protein_content: parameters.initial_protein_content,
            output_protein_content: parameters.output_protein_content,
            process_type: parameters.process_type,
            moisture_compensation_factor: parameters.moisture_compensation_factor,
            initial_moisture: parameters.initial_moisture,
            final_moisture: parameters.final_moisture
          },
          separation_input: {
            feed_composition: parameters.feed_composition,
            product_composition: parameters.product_composition,
            mass_flow: parameters.mass_flow,
            process_data: [{
              feed_composition: parameters.feed_composition,
              product_composition: parameters.product_composition,
              mass_flow: parameters.mass_flow,
              processing_moisture: parameters.final_moisture
            }],
            target_purity: parameters.target_purity
          },
          particle_input: {
            particle_sizes: parameters.particle_sizes,
            weights: parameters.weights,
            density: parameters.density,
            target_ranges: parameters.target_ranges,
            initial_moisture: parameters.initial_moisture,
            final_moisture: parameters.final_moisture,
            treatment_type: parameters.treatment_type
          }
        })
      });

      if (!response.ok) {
        const errorData = await response.json();
        console.error('Analysis failed:', errorData);
        throw new Error(errorData.detail?.message || errorData.detail || 'Analysis failed');
      }

      const data = await response.json();
      console.log('Analysis results:', data);
      setResults(data);
      setActiveTab("results");
      
      toast({
        title: "Analysis Complete",
        description: "Technical analysis results are ready for review.",
      });
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Failed to perform analysis';
      console.error('Analysis error:', err);
      setError(message);
      toast({
        variant: "destructive",
        title: "Analysis Failed",
        description: message,
      });
    } finally {
      setIsAnalyzing(false);
    }
  };

  return (
    <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
      <TabsList className="grid w-full grid-cols-2 mb-6">
        <TabsTrigger value="input">Input Parameters</TabsTrigger>
        <TabsTrigger value="results" disabled={!results}>Analysis Results</TabsTrigger>
      </TabsList>

      <TabsContent value="input" className="space-y-6">
        <Card className="p-6">
          <TechnicalInputForm
            onSubmit={handleAnalysis}
            isSubmitting={isAnalyzing}
          />
        </Card>
      </TabsContent>

      <TabsContent value="results" className="space-y-6">
        <TechnicalAnalysisView
          data={results}
          isLoading={isAnalyzing}
          error={error}
        />
      </TabsContent>
    </Tabs>
  );
}

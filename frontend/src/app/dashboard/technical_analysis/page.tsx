"use client";

import React, { useState } from 'react';
import TechnicalInputForm from "@/components/forms/TechnicalInputForm";
import { TechnicalAnalysisView } from "@/features/analysis/technical/components/TechnicalAnalysisView";
import { TechnicalParameters, TechnicalResults } from "@/types/technical";
import { API_CONFIG, API_ENDPOINTS } from "@/config/api";
import { useToast } from "@/components/ui/use-toast";
import { Card } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { AnimatePresence } from "framer-motion";
import { MotionDiv } from "@/components/motion";
import { Loader2, AlertCircle } from 'lucide-react';
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { Progress } from "@/components/ui/progress";

export default function TechnicalAnalysisPage() {
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [results, setResults] = useState<TechnicalResults | undefined>();
  const [error, setError] = useState<string | undefined>();
  const [activeTab, setActiveTab] = useState<string>("input");
  const [progress, setProgress] = useState(0);
  const { toast } = useToast();

  const simulateProgress = () => {
    setProgress(0);
    const interval = setInterval(() => {
      setProgress((prev) => {
        if (prev >= 90) {
          clearInterval(interval);
          return prev;
        }
        return prev + 10;
      });
    }, 500);
    return interval;
  };

  const handleAnalysis = async (parameters: TechnicalParameters) => {
    setIsAnalyzing(true);
    setError(undefined);
    const progressInterval = simulateProgress();
    
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
      
      // Complete the progress bar
      setProgress(100);
      clearInterval(progressInterval);
      
      // Short delay before showing results
      await new Promise(resolve => setTimeout(resolve, 500));
      
      setResults(data);
      setActiveTab("results");
      
      toast({
        title: "Analysis Complete",
        description: "Technical analysis results are ready for review.",
        variant: "default",
      });
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Failed to perform analysis';
      console.error('Analysis error:', err);
      setError(message);
      clearInterval(progressInterval);
      setProgress(0);
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
    <div className="space-y-6">
      <Tabs 
        value={activeTab} 
        onValueChange={setActiveTab} 
        className="w-full"
      >
        <TabsList className="grid w-full grid-cols-2 mb-6">
          <TabsTrigger 
            value="input"
            disabled={isAnalyzing}
            className="data-[state=active]:bg-primary data-[state=active]:text-primary-foreground"
          >
            Input Parameters
          </TabsTrigger>
          <TabsTrigger 
            value="results" 
            disabled={!results || isAnalyzing}
            className="data-[state=active]:bg-primary data-[state=active]:text-primary-foreground"
          >
            Analysis Results
          </TabsTrigger>
        </TabsList>

        <AnimatePresence mode="wait">
          {isAnalyzing && (
            <MotionDiv
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              className="space-y-4"
            >
              <Card className="p-6">
                <div className="flex items-center space-x-4">
                  <Loader2 className="h-5 w-5 animate-spin text-primary" />
                  <div className="space-y-2 flex-1">
                    <h4 className="font-medium">Analyzing protein process data...</h4>
                    <Progress value={progress} className="h-2" />
                  </div>
                </div>
              </Card>
            </MotionDiv>
          )}

          <TabsContent value="input" className="space-y-6 mt-0">
            <MotionDiv
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
            >
              <Card className="p-6">
                <TechnicalInputForm
                  onSubmit={handleAnalysis}
                  isSubmitting={isAnalyzing}
                />
              </Card>
            </MotionDiv>
          </TabsContent>

          <TabsContent value="results" className="space-y-6 mt-0">
            {error ? (
              <MotionDiv
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                exit={{ opacity: 0, scale: 0.95 }}
              >
                <Alert variant="destructive">
                  <AlertCircle className="h-4 w-4" />
                  <AlertTitle>Error</AlertTitle>
                  <AlertDescription>
                    {error}
                    <button 
                      onClick={() => {
                        setError(undefined);
                        setActiveTab("input");
                      }}
                      className="underline ml-2 hover:text-muted-foreground"
                    >
                      Return to input form
                    </button>
                  </AlertDescription>
                </Alert>
              </MotionDiv>
            ) : (
              <MotionDiv
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
              >
                <TechnicalAnalysisView
                  data={results}
                  isLoading={isAnalyzing}
                  error={error}
                />
              </MotionDiv>
            )}
          </TabsContent>
        </AnimatePresence>
      </Tabs>
    </div>
  );
}

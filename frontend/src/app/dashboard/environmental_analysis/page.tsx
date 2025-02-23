"use client";

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import { Alert, AlertTitle, AlertDescription } from "@/components/ui/alert";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { EnvironmentalInputForm } from '@/components/forms/EnvironmentalInputForm';
import { EnvironmentalAnalysisView } from '@/features/analysis/environmental/components/EnvironmentalAnalysisView';
import { EnvironmentalAnalysisRequest, EnvironmentalAnalysisResponse } from '@/types/environmental';
import { API_ENDPOINTS, API_CONFIG } from '@/config/api';
import AnalysisLayout from '@/components/layout/AnalysisLayout';
import { Loader2 } from 'lucide-react';

export default function EnvironmentalAnalysisPage() {
  const router = useRouter();
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [results, setResults] = useState<EnvironmentalAnalysisResponse | null>(null);
  const [activeTab, setActiveTab] = useState<string>("input");

  const handleSubmit = async (values: EnvironmentalAnalysisRequest) => {
    setIsSubmitting(true);
    setError(null);

    try {
      const response = await fetch(API_ENDPOINTS.environmental.analyze, {
        method: 'POST',
        ...API_CONFIG,
        body: JSON.stringify(values),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail?.message || 'Failed to perform environmental analysis');
      }

      const data = await response.json();
      setResults(data);
      setActiveTab("results");
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An unexpected error occurred');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <AnalysisLayout>
      {error && (
        <Alert variant="destructive" className="mb-6 animate-in fade-in slide-in-from-top-2 duration-300">
          <AlertTitle>Error</AlertTitle>
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}

      <Tabs 
        value={activeTab} 
        onValueChange={setActiveTab}
        className="animate-in fade-in duration-500"
      >
        <div className="flex items-center justify-between mb-6">
          <TabsList className="grid w-[400px] grid-cols-2">
            <TabsTrigger value="input" className="data-[state=active]:bg-primary data-[state=active]:text-primary-foreground">
              Process Parameters
            </TabsTrigger>
            <TabsTrigger 
              value="results" 
              disabled={!results}
              className="data-[state=active]:bg-primary data-[state=active]:text-primary-foreground"
            >
              Impact Assessment
            </TabsTrigger>
          </TabsList>

          {isSubmitting && (
            <div className="flex items-center gap-2 text-sm text-muted-foreground">
              <Loader2 className="w-4 h-4 animate-spin" />
              Analyzing Environmental Impact...
            </div>
          )}
        </div>

        <TabsContent 
          value="input"
          className="animate-in fade-in-50 duration-500"
        >
          <EnvironmentalInputForm
            onSubmit={handleSubmit}
            isLoading={isSubmitting}
          />
        </TabsContent>

        <TabsContent 
          value="results"
          className="animate-in fade-in-50 duration-500"
        >
          {results && (
            <EnvironmentalAnalysisView 
              data={results}
              error={error || undefined}
            />
          )}
        </TabsContent>
      </Tabs>
    </AnalysisLayout>
  );
}

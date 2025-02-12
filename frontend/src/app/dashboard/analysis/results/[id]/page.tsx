import React from 'react';
import { AnalysisResultsClient } from './AnalysisResultsClient';
import { headers } from 'next/headers';
import { AnalysisResult } from '@/types/api';
import { ProcessStatus } from '@/types/process';
import { API_ENDPOINTS } from '@/config/api';

// Helper function to safely serialize nested objects
function serializeNestedObject(obj: any): any {
  if (!obj) return undefined;
  if (typeof obj !== 'object') return obj;
  
  // Handle Date objects
  if (obj instanceof Date) {
    return obj.toISOString();
  }
  
  const result: any = {};
  for (const [key, value] of Object.entries(obj)) {
    if (value === null || value === undefined) {
      continue; // Skip null/undefined values
    } else if (Array.isArray(value)) {
      result[key] = value.map(item => serializeNestedObject(item));
    } else if (typeof value === 'object') {
      const serialized = serializeNestedObject(value);
      if (serialized !== undefined) {
        result[key] = serialized;
      }
    } else {
      result[key] = value;
    }
  }
  return Object.keys(result).length > 0 ? result : undefined;
}

async function getAnalysisData(id: string): Promise<AnalysisResult | null> {
  try {
    const headersList = headers();
    const token = headersList.get('authorization');

    if (!token) {
      console.error('No authorization token found');
      return {
        status: ProcessStatus.FAILED,
        progress: 0,
        results: undefined
      };
    }
    
    const response = await fetch(API_ENDPOINTS.process.results(id), {
      headers: {
        'Authorization': token,
        'Content-Type': 'application/json',
      },
      cache: 'no-store'
    });

    if (!response.ok) {
      console.error('API Error:', {
        status: response.status,
        statusText: response.statusText,
        url: response.url
      });
      
      return {
        status: ProcessStatus.FAILED,
        progress: 0,
        results: undefined
      };
    }

    const rawData = await response.json();
    
    // Log the raw data structure for debugging
    console.log('Raw API Response:', {
      status: response.status,
      headers: Object.fromEntries(response.headers.entries()),
      data: rawData
    });

    // Create a new object with explicit serialization
    const serializedData: AnalysisResult = {
      status: rawData.status || ProcessStatus.PENDING,
      progress: typeof rawData.progress === 'number' ? rawData.progress : 0,
      results: rawData.results ? {
        technical: serializeNestedObject(rawData.results.technical),
        economic: serializeNestedObject(rawData.results.economic),
        environmental: serializeNestedObject(rawData.results.environmental)
      } : undefined
    };

    // Validate the serialized data
    console.log('Serialized Data:', JSON.stringify(serializedData, null, 2));

    return serializedData;
  } catch (error) {
    console.error('Error in getAnalysisData:', error);
    return {
      status: ProcessStatus.FAILED,
      progress: 0,
      results: undefined
    };
  }
}

export default async function AnalysisResultsPage({ params }: { params: { id: string } }) {
  const analysisId = String(params.id);
  const initialData = await getAnalysisData(analysisId);

  return (
    <AnalysisResultsClient 
      analysisId={analysisId} 
      initialData={initialData}
    />
  );
} 
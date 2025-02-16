"use client";

import React from 'react';
import { Button } from "@/components/ui/button";
import { ArrowLeft } from "lucide-react";
import Link from "next/link";

interface AnalysisResultsLayoutProps {
  children: React.ReactNode;
}

export default function AnalysisResultsLayout({ children }: AnalysisResultsLayoutProps) {
  return (
    <div>
      <div className="border-b">
        <div className="flex h-16 items-center px-4">
          <Link href="/dashboard/analysis" passHref>
            <Button variant="ghost" className="gap-2">
              <ArrowLeft className="h-4 w-4" />
              Back to Analysis
            </Button>
          </Link>
          <div className="ml-auto flex items-center space-x-4">
            <h1 className="text-lg font-semibold">Analysis Results</h1>
          </div>
        </div>
      </div>
      <div className="flex-1">
        {children}
      </div>
    </div>
  );
} 
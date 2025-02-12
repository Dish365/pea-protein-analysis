"use client";

import React from 'react';
import { useRouter } from 'next/navigation';
import { formatDistanceToNow } from 'date-fns';
import { RefreshCw, Eye, Beaker, DollarSign, Leaf } from 'lucide-react';
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { useRecentAnalyses, RecentAnalysis } from '@/hooks/useRecentAnalyses';
import { Alert, AlertDescription } from "@/components/ui/alert";
import { ProcessType, ProcessStatus } from '@/types/process';

type ProcessTypeKey = Lowercase<keyof typeof ProcessType>;

const analysisTypeConfig: Record<ProcessTypeKey, {
  icon: React.ReactNode;
  label: string;
}> = {
  baseline: {
    icon: <Beaker className="h-4 w-4" />,
    label: 'Baseline Analysis'
  },
  rf: {
    icon: <DollarSign className="h-4 w-4" />,
    label: 'RF Process Analysis'
  },
  ir: {
    icon: <Leaf className="h-4 w-4" />,
    label: 'IR Process Analysis'
  },
};

const statusConfig = {
  [ProcessStatus.PENDING]: {
    variant: 'secondary' as const,
    label: 'Pending'
  },
  [ProcessStatus.PROCESSING]: {
    variant: 'default' as const,
    label: 'Processing'
  },
  [ProcessStatus.COMPLETED]: {
    variant: 'success' as const,
    label: 'Completed'
  },
  [ProcessStatus.FAILED]: {
    variant: 'destructive' as const,
    label: 'Failed'
  },
} as const;

export function RecentAnalyses() {
  const router = useRouter();
  const { data, isLoading, error, refetch } = useRecentAnalyses();
  const analyses = data?.items as RecentAnalysis[] | undefined;

  if (error) {
    return (
      <Alert variant="destructive">
        <AlertDescription>Failed to load recent analyses</AlertDescription>
      </Alert>
    );
  }

  const getAnalysisConfig = (type: ProcessType) => {
    const key = type.toLowerCase() as ProcessTypeKey;
    return analysisTypeConfig[key];
  };

  return (
    <Card>
      <CardHeader>
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <CardTitle>Recent Analyses</CardTitle>
            <Button
              variant="ghost"
              size="icon"
              onClick={() => refetch()}
              disabled={isLoading}
            >
              <RefreshCw className="h-4 w-4" />
            </Button>
          </div>
          <Button
            variant="link"
            onClick={() => router.push('/analysis/history')}
          >
            View All
          </Button>
        </div>
        <CardDescription>Your most recent analysis runs</CardDescription>
      </CardHeader>
      <CardContent>
        {isLoading ? (
          <div className="space-y-4">
            {[...Array(3)].map((_, i) => (
              <div key={i} className="animate-pulse">
                <div className="h-16 bg-muted rounded-md" />
              </div>
            ))}
          </div>
        ) : (
          <div className="h-[400px] overflow-auto pr-4">
            <div className="space-y-4">
              {(analyses || []).map((analysis) => (
                <div
                  key={analysis.id}
                  className="flex items-center justify-between p-4 rounded-lg border"
                >
                  <div className="flex items-center gap-4">
                    <div className="p-2 rounded-full bg-muted">
                      {getAnalysisConfig(analysis.type).icon}
                    </div>
                    <div>
                      <p className="font-medium">
                        {getAnalysisConfig(analysis.type).label}
                      </p>
                      <p className="text-sm text-muted-foreground">
                        {formatDistanceToNow(new Date(analysis.created_at), { addSuffix: true })}
                      </p>
                    </div>
                  </div>
                  <div className="flex items-center gap-4">
                    <div className="w-32">
                      <Progress value={analysis.progress} />
                    </div>
                    <Badge variant={statusConfig[analysis.status].variant}>
                      {statusConfig[analysis.status].label}
                    </Badge>
                    <Button
                      variant="ghost"
                      size="icon"
                      onClick={() => router.push(`/analysis/${analysis.id}`)}
                    >
                      <Eye className="h-4 w-4" />
                    </Button>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </CardContent>
    </Card>
  );
}

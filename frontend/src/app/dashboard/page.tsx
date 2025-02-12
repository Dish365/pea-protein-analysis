"use client";

import React from "react";
import { Activity, DollarSign, Leaf, Loader2 } from "lucide-react";
import { AnalysisCard } from "@/components/dashboard/AnalysisCard";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { useRecentAnalyses } from "@/hooks/useRecentAnalyses";
import { ProcessStatus, ProcessType } from "@/types/process";
import { format } from "date-fns";
import { useRouter } from "next/navigation";

export default function DashboardPage() {
  const router = useRouter();
  const { data: recentAnalyses, isLoading } = useRecentAnalyses(1, 10);

  // Calculate metrics for each process type
  const getProcessMetrics = (processType: ProcessType) => {
    if (!recentAnalyses?.items) return { completed: 0, inProgress: 0, trend: 0 };

    const processAnalyses = recentAnalyses.items.filter(
      (analysis) => analysis.process_type === processType
    );

    const completed = processAnalyses.filter(
      (a) => a.status === ProcessStatus.COMPLETED
    ).length;
    const inProgress = processAnalyses.filter(
      (a) => a.status === ProcessStatus.PROCESSING || a.status === ProcessStatus.PENDING
    ).length;

    // Calculate trend (comparing with previous period)
    const recentCompleted = processAnalyses
      .filter((a) => {
        const date = new Date(a.timestamp);
        const oneWeekAgo = new Date();
        oneWeekAgo.setDate(oneWeekAgo.getDate() - 7);
        return date >= oneWeekAgo && a.status === ProcessStatus.COMPLETED;
      }).length;

    const olderCompleted = processAnalyses
      .filter((a) => {
        const date = new Date(a.timestamp);
        const twoWeeksAgo = new Date();
        const oneWeekAgo = new Date();
        twoWeeksAgo.setDate(twoWeeksAgo.getDate() - 14);
        oneWeekAgo.setDate(oneWeekAgo.getDate() - 7);
        return date >= twoWeeksAgo && date < oneWeekAgo && a.status === ProcessStatus.COMPLETED;
      }).length;

    const trend = olderCompleted === 0 
      ? recentCompleted * 100 
      : Math.round(((recentCompleted - olderCompleted) / olderCompleted) * 100);

    return { completed, inProgress, trend };
  };

  const analysisOverviews = [
    {
      title: "Baseline Analysis",
      description: "Standard pea protein extraction process",
      icon: <Activity className="h-6 w-6" />,
      color: "#1e40af",
      variant: "default" as const,
      metrics: getProcessMetrics(ProcessType.BASELINE),
      onClick: () => router.push("/dashboard/analysis"),
    },
    {
      title: "RF Analysis",
      description: "Radio frequency assisted extraction",
      icon: <DollarSign className="h-6 w-6" />,
      color: "#15803d",
      variant: "success" as const,
      metrics: getProcessMetrics(ProcessType.RF),
      onClick: () => router.push("/dashboard/analysis"),
    },
    {
      title: "IR Analysis",
      description: "Infrared assisted extraction",
      icon: <Leaf className="h-6 w-6" />,
      color: "#7e22ce",
      variant: "warning" as const,
      metrics: getProcessMetrics(ProcessType.IR),
      onClick: () => router.push("/dashboard/analysis"),
    },
  ];

  const getStatusColor = (status: ProcessStatus) => {
    switch (status) {
      case ProcessStatus.COMPLETED:
        return "success";
      case ProcessStatus.PROCESSING:
        return "default";
      case ProcessStatus.FAILED:
        return "destructive";
      default:
        return "secondary";
    }
  };

  const getProcessTypeIcon = (type: ProcessType) => {
    switch (type) {
      case ProcessType.BASELINE:
        return <Activity className="h-4 w-4" />;
      case ProcessType.RF:
        return <DollarSign className="h-4 w-4" />;
      case ProcessType.IR:
        return <Leaf className="h-4 w-4" />;
    }
  };

  const getProcessTypeColor = (type: ProcessType) => {
    switch (type) {
      case ProcessType.BASELINE:
        return { bg: "#1e40af20", text: "#1e40af" };
      case ProcessType.RF:
        return { bg: "#15803d20", text: "#15803d" };
      case ProcessType.IR:
        return { bg: "#7e22ce20", text: "#7e22ce" };
    }
  };

  return (
    <div className="space-y-6">
      {/* Analysis Overview Cards */}
      <div className="grid gap-6 md:grid-cols-3">
        {analysisOverviews.map((analysis) => (
          <AnalysisCard key={analysis.title} {...analysis} />
        ))}
      </div>

      {/* Recent Analyses */}
      <Card>
        <CardHeader>
          <CardTitle>Recently Performed Analyses</CardTitle>
        </CardHeader>
        <CardContent>
          {isLoading ? (
            <div className="flex items-center justify-center p-8">
              <Loader2 className="h-8 w-8 animate-spin text-muted-foreground" />
            </div>
          ) : recentAnalyses?.items && recentAnalyses.items.length > 0 ? (
            <div className="space-y-4">
              {recentAnalyses.items.map((analysis) => (
                <div
                  key={analysis.id}
                  className="flex items-center justify-between p-4 border rounded-lg hover:bg-accent/50 cursor-pointer transition-colors"
                  onClick={() => router.push(`/dashboard/analysis/results/${analysis.id}`)}
                >
                  <div className="flex items-center gap-4">
                    <div
                      className="p-2 rounded-full"
                      style={{
                        backgroundColor: getProcessTypeColor(analysis.process_type).bg,
                        color: getProcessTypeColor(analysis.process_type).text,
                      }}
                    >
                      {getProcessTypeIcon(analysis.process_type)}
                    </div>
                    <div>
                      <p className="font-medium">
                        {analysis.process_type.toUpperCase()} Analysis
                      </p>
                      <p className="text-sm text-muted-foreground">
                        {format(new Date(analysis.timestamp), 'PPp')}
                      </p>
                    </div>
                  </div>
                  <div className="flex items-center gap-4">
                    <div className="w-32">
                      <Progress
                        value={analysis.progress}
                        className={
                          analysis.status === ProcessStatus.COMPLETED
                            ? "bg-emerald-100"
                            : analysis.status === ProcessStatus.FAILED
                            ? "bg-red-100"
                            : "bg-blue-100"
                        }
                        indicatorColor={
                          analysis.status === ProcessStatus.COMPLETED
                            ? "rgb(16 185 129)"
                            : analysis.status === ProcessStatus.FAILED
                            ? "rgb(239 68 68)"
                            : "rgb(59 130 246)"
                        }
                      />
                    </div>
                    <Badge variant={getStatusColor(analysis.status)}>
                      {analysis.status}
                    </Badge>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="flex items-center justify-center p-8 text-muted-foreground">
              No analyses performed yet
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
} 
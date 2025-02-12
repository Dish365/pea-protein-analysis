"use client";

import React from "react";
import { Activity, DollarSign, Leaf } from "lucide-react";
import { AnalysisCard } from "@/components/dashboard/AnalysisCard";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";

const analysisOverviews = [
  {
    title: "Technical Analysis",
    description: "Process optimization and efficiency metrics",
    icon: <Activity className="h-6 w-6" />,
    color: "#1e40af",
    metrics: {
      completed: 24,
      inProgress: 3,
      trend: 8,
    },
    onClick: () => window.location.href = "/dashboard/analysis/technical",
  },
  {
    title: "Economic Analysis",
    description: "Cost and profitability assessment",
    icon: <DollarSign className="h-6 w-6" />,
    color: "#15803d",
    metrics: {
      completed: 18,
      inProgress: 2,
      trend: 12,
    },
    onClick: () => window.location.href = "/dashboard/analysis/economic",
  },
  {
    title: "Environmental Analysis",
    description: "Sustainability and environmental impact",
    icon: <Leaf className="h-6 w-6" />,
    color: "#7e22ce",
    metrics: {
      completed: 15,
      inProgress: 4,
      trend: -5,
    },
    onClick: () => window.location.href = "/dashboard/analysis/environmental",
  },
];

const recentAnalyses = [
  {
    id: "1",
    name: "Protein Extraction Process",
    type: "technical",
    date: "2024-01-30",
    progress: 92,
    status: "Complete",
  },
  {
    id: "2",
    name: "Cost Analysis Q1 2024",
    type: "economic",
    date: "2024-01-29",
    progress: 68,
    status: "Complete",
  },
  {
    id: "3",
    name: "Carbon Footprint Assessment",
    type: "environmental",
    date: "2024-01-28",
    progress: 73,
    status: "In Progress",
  },
];

export default function DashboardPage() {
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
          <div className="space-y-4">
            {recentAnalyses.map((item) => (
              <div
                key={item.id}
                className="flex items-center justify-between p-4 border rounded-lg"
              >
                <div className="flex items-center gap-4">
                  <div
                    className="p-2 rounded-full"
                    style={{
                      backgroundColor:
                        item.type === "technical"
                          ? "#1e40af20"
                          : item.type === "economic"
                          ? "#15803d20"
                          : "#7e22ce20",
                      color:
                        item.type === "technical"
                          ? "#1e40af"
                          : item.type === "economic"
                          ? "#15803d"
                          : "#7e22ce",
                    }}
                  >
                    {item.type === "technical" && <Activity className="h-4 w-4" />}
                    {item.type === "economic" && <DollarSign className="h-4 w-4" />}
                    {item.type === "environmental" && <Leaf className="h-4 w-4" />}
                  </div>
                  <div>
                    <p className="font-medium">{item.name}</p>
                    <p className="text-sm text-muted-foreground">{item.date}</p>
                  </div>
                </div>
                <div className="flex items-center gap-4">
                  <div className="w-32">
                    <Progress
                      value={item.progress}
                      className={item.status === "Complete" ? "bg-emerald-100" : "bg-blue-100"}
                      indicatorColor={
                        item.status === "Complete"
                          ? "rgb(16 185 129)"
                          : "rgb(59 130 246)"
                      }
                    />
                  </div>
                  <Badge
                    variant={item.status === "Complete" ? "success" : "default"}
                  >
                    {item.status}
                  </Badge>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );
} 
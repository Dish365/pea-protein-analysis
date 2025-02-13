"use client";

import React from 'react';
import DashboardLayout from '@/components/layout/DashboardLayout';
import { RecentAnalyses } from '@/components/dashboard/RecentAnalyses';
import { AnalysisCard } from '@/components/dashboard/AnalysisCard';
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Activity, ArrowRight, BarChart3, DollarSign, FileText, Leaf } from 'lucide-react';
import { Button } from '@/components/ui/button';
import Link from 'next/link';

export default function DashboardPage() {
  const content = (
    <div className="flex flex-col gap-8">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Dashboard</h1>
          <p className="text-muted-foreground">
            Overview of your process analysis activities
          </p>
        </div>
        <Button asChild>
          <Link href="/dashboard/analysis" className="gap-2">
            New Analysis
            <ArrowRight className="h-4 w-4" />
          </Link>
        </Button>
      </div>

      {/* Quick Stats */}
      <div className="grid gap-4 md:grid-cols-3">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2 space-y-0">
            <CardTitle className="text-sm font-medium">Total Analyses</CardTitle>
            <BarChart3 className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">128</div>
            <p className="text-xs text-muted-foreground">
              +14% from last month
            </p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2 space-y-0">
            <CardTitle className="text-sm font-medium">Success Rate</CardTitle>
            <Activity className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">92.6%</div>
            <p className="text-xs text-muted-foreground">
              +2.1% from last month
            </p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2 space-y-0">
            <CardTitle className="text-sm font-medium">Active Projects</CardTitle>
            <FileText className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">12</div>
            <p className="text-xs text-muted-foreground">
              3 pending review
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Main Content */}
      <Tabs defaultValue="overview" className="space-y-6">
        <TabsList>
          <TabsTrigger value="overview">Performance Overview</TabsTrigger>
          <TabsTrigger value="analyses">Recent Analyses</TabsTrigger>
        </TabsList>

        <TabsContent value="overview" className="space-y-6">
          <div className="grid gap-4 md:grid-cols-3">
            <AnalysisCard
              title="Technical Performance"
              description="Process efficiency metrics"
              icon={<Activity className="h-5 w-5 text-blue-500" />}
              variant="default"
              metrics={{
                completed: 85,
                inProgress: 5,
                trend: 2.5
              }}
              onClick={() => {}}
            />
            <AnalysisCard
              title="Economic Metrics"
              description="Cost and profitability analysis"
              icon={<DollarSign className="h-5 w-5 text-green-500" />}
              variant="success"
              metrics={{
                completed: 92,
                inProgress: 8,
                trend: 4.2
              }}
              onClick={() => {}}
            />
            <AnalysisCard
              title="Environmental Impact"
              description="Sustainability indicators"
              icon={<Leaf className="h-5 w-5 text-emerald-500" />}
              variant="success"
              metrics={{
                completed: 88,
                inProgress: 12,
                trend: -12
              }}
              onClick={() => {}}
            />
          </div>

          <Card>
            <CardHeader>
              <CardTitle>Analysis Distribution</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="h-[200px] flex items-center justify-center text-muted-foreground">
                Chart placeholder
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="analyses">
          <Card>
            <CardHeader>
              <CardTitle>Recent Analyses</CardTitle>
            </CardHeader>
            <CardContent>
              <RecentAnalyses />
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );

  return <DashboardLayout>{content}</DashboardLayout>;
} 
"use client"

import React from 'react'
import { TrendingUp, TrendingDown } from 'lucide-react'
import { Button } from "@/components/ui/button"
import { Progress } from "@/components/ui/progress"
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from "@/components/ui/tooltip"

interface AnalysisCardProps {
  title: string
  description: string
  icon: React.ReactNode
  color: string
  metrics: {
    completed: number
    inProgress: number
    trend?: number // Percentage change from last period
  }
  onClick: () => void
}

export function AnalysisCard({
  title,
  description,
  icon,
  color,
  metrics,
  onClick,
}: AnalysisCardProps) {
  const totalAnalyses = metrics.completed + metrics.inProgress
  const completionRate = (metrics.completed / totalAnalyses) * 100

  return (
    <Card className="h-full" style={{ borderTop: `2px solid ${color}` }}>
      <CardHeader>
        <div className="flex items-start gap-4">
          <div
            className="p-2 rounded-lg"
            style={{ backgroundColor: `${color}20` }}
          >
            {icon}
          </div>
          <div>
            <CardTitle>{title}</CardTitle>
            <CardDescription>{description}</CardDescription>
          </div>
        </div>
      </CardHeader>
      <CardContent className="space-y-6">
        <TooltipProvider>
          <Tooltip>
            <TooltipTrigger asChild>
              <div>
                <Progress value={completionRate} indicatorColor={color} />
              </div>
            </TooltipTrigger>
            <TooltipContent>
              <p>Analysis completion rate: {Math.round(completionRate)}%</p>
            </TooltipContent>
          </Tooltip>
        </TooltipProvider>

        <div className="grid grid-cols-2 gap-4">
          <div>
            <p className="text-sm text-muted-foreground">Completed</p>
            <p className="text-2xl font-semibold" style={{ color }}>
              {metrics.completed}
            </p>
          </div>
          <div>
            <p className="text-sm text-muted-foreground">In Progress</p>
            <p className="text-2xl font-semibold" style={{ color: '#faad14' }}>
              {metrics.inProgress}
            </p>
          </div>
        </div>

        {metrics.trend !== undefined && (
          <div>
            <p className="text-sm text-muted-foreground">Trend</p>
            <div className="flex items-center gap-2">
              {metrics.trend > 0 ? (
                <TrendingUp className="text-emerald-500" />
              ) : (
                <TrendingDown className="text-red-500" />
              )}
              <p
                className="text-2xl font-semibold"
                style={{
                  color: metrics.trend > 0 ? '#10b981' : '#ef4444',
                }}
              >
                {metrics.trend}%
              </p>
            </div>
          </div>
        )}
      </CardContent>
      <CardFooter>
        <Button
          className="w-full"
          onClick={onClick}
          style={{
            backgroundColor: color,
            borderColor: color,
          }}
        >
          Start New Analysis
        </Button>
      </CardFooter>
    </Card>
  )
} 
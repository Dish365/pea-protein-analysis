"use client"

import * as React from "react"
import { cn } from "@/lib/utils"
import { Loader2, AlertCircle } from "lucide-react"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { Progress } from "@/components/ui/progress"
import { ProcessStatus } from "@/types/process"

interface LoadingSpinnerProps {
  tip?: string
  subTip?: string
  progress?: number
  size?: 'sm' | 'default' | 'lg'
  fullscreen?: boolean
  className?: string
  overlay?: boolean
  status?: ProcessStatus
  error?: string
  showProgress?: boolean
  progressSteps?: Array<{
    label: string
    progress: number
    status: ProcessStatus
  }>
}

export function LoadingSpinner({
  tip = 'Loading...',
  subTip,
  progress,
  size = 'default',
  fullscreen = false,
  overlay = false,
  className,
  status = ProcessStatus.PROCESSING,
  error,
  showProgress = true,
  progressSteps,
}: LoadingSpinnerProps) {
  const spinnerSize = {
    sm: 'w-4 h-4',
    default: 'w-6 h-6',
    lg: 'w-8 h-8'
  }[size]

  const textSize = {
    sm: 'text-sm',
    default: 'text-base',
    lg: 'text-lg'
  }[size]

  const containerClasses = cn(
    'flex flex-col items-center justify-center gap-4',
    (fullscreen || overlay) && 'fixed inset-0 bg-background/80 backdrop-blur-sm z-50',
    !fullscreen && !overlay && 'p-8',
    className
  )

  if (error) {
    return (
      <div className={containerClasses}>
        <Alert variant="destructive">
          <AlertCircle className="h-4 w-4" />
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      </div>
    )
  }

  const statusColor = {
    [ProcessStatus.PENDING]: 'text-muted-foreground',
    [ProcessStatus.PROCESSING]: 'text-primary',
    [ProcessStatus.COMPLETED]: 'text-emerald-500',
    [ProcessStatus.FAILED]: 'text-destructive'
  }[status]

  return (
    <div className={containerClasses}>
      <Loader2 className={cn("animate-spin", spinnerSize, statusColor)} />
      <p className={cn("font-semibold", textSize, statusColor)}>
        {tip}
      </p>
      {showProgress && progress !== undefined && (
        <div className="w-full max-w-[300px]">
          <Progress value={progress} className="h-2" />
          <p className="text-sm text-muted-foreground text-center mt-1">
            {Math.round(progress)}%
          </p>
        </div>
      )}
      {progressSteps && (
        <div className="w-full max-w-[300px] space-y-3">
          {progressSteps.map((step, index) => (
            <div key={index} className="space-y-1">
              <div className="flex justify-between text-sm">
                <span className="text-muted-foreground">{step.label}</span>
                <span className={cn(
                  "font-medium",
                  {
                    [ProcessStatus.PENDING]: 'text-muted-foreground',
                    [ProcessStatus.PROCESSING]: 'text-primary',
                    [ProcessStatus.COMPLETED]: 'text-emerald-500',
                    [ProcessStatus.FAILED]: 'text-destructive'
                  }[step.status]
                )}>
                  {step.progress}%
                </span>
              </div>
              <Progress 
                value={step.progress} 
                className={cn(
                  "h-1.5",
                  step.status === ProcessStatus.COMPLETED && "bg-emerald-100",
                  step.status === ProcessStatus.FAILED && "bg-destructive/20"
                )}
              />
            </div>
          ))}
        </div>
      )}
      {subTip && (
        <p className="text-sm text-muted-foreground">
          {subTip}
        </p>
      )}
    </div>
  )
} 
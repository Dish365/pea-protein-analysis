"use client"

import * as React from "react"
import { cn } from "@/lib/utils"
import { Loader2 } from "lucide-react"

interface LoadingSpinnerProps {
  tip?: string
  subTip?: string
  progress?: number
  size?: 'sm' | 'default' | 'lg'
  fullscreen?: boolean
  className?: string
}

export function LoadingSpinner({
  tip = 'Loading...',
  subTip,
  progress,
  size = 'default',
  fullscreen = false,
  className,
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

  return (
    <div className={cn(
      'flex flex-col items-center justify-center gap-4',
      fullscreen && 'fixed inset-0 bg-background/80 backdrop-blur-sm z-50',
      !fullscreen && 'p-8',
      className
    )}>
      <Loader2 className={cn("animate-spin", spinnerSize)} />
      <p className={cn("font-semibold", textSize)}>
        {tip}
      </p>
      {progress !== undefined && (
        <div className="w-full max-w-[200px]">
          <div className="h-2 bg-secondary rounded-full overflow-hidden">
            <div 
              className="h-full bg-primary transition-all duration-300"
              style={{ width: `${progress}%` }}
            />
          </div>
          <p className="text-sm text-muted-foreground text-center mt-1">
            {progress}%
          </p>
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
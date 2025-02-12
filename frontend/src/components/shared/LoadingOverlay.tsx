"use client"

import React from 'react'
import { LoadingSpinner } from "@/components/ui/loading-spinner"

interface LoadingOverlayProps {
  tip?: string
  subTip?: string
  progress?: number
}

const LoadingOverlay: React.FC<LoadingOverlayProps> = ({
  tip,
  subTip,
  progress
}) => {
  return (
    <LoadingSpinner
      tip={tip}
      subTip={subTip}
      progress={progress}
      size="lg"
      fullscreen
    />
  )
}

export default LoadingOverlay 
"use client"

import { LoadingSpinner } from "./loading-spinner"

export function LoadingOverlay(props: React.ComponentProps<typeof LoadingSpinner>) {
  return <LoadingSpinner {...props} overlay fullscreen />
}

export function PageLoading() {
  return <LoadingSpinner fullscreen />
}

export function SectionLoading() {
  return <LoadingSpinner size="sm" />
}

export { LoadingSpinner } 
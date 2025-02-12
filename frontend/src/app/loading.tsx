import React from "react";
import { LoadingSpinner } from "@/components/ui/loading-spinner";

export default function Loading(): React.JSX.Element {
  return <LoadingSpinner tip="Loading application..." />;
}

import React from "react";
import { LoadingSpinner } from "@/components/ui/loading-spinner";

export default function Loading(): React.JSX.Element {
  return <LoadingSpinner fullscreen tip="Loading..." />;
}

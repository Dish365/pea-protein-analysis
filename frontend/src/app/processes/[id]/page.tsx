"use client";
import React from "react";
import { useParams } from "next/navigation";

export default function ProcessDetailsPage() {
  const params = useParams();
  const processId = params.id;

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Process Details</h1>
      <p>Process ID: {processId}</p>
      {/* Process details content will go here */}
    </div>
  );
}

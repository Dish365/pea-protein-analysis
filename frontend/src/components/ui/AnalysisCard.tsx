"use client";

import React from "react";
import { Card, Progress } from "antd";

interface Metrics {
  completed: number;
  inProgress: number;
  trend?: number;
}

interface AnalysisCardProps {
  title: string;
  description: string;
  icon: React.ReactNode;
  color: string;
  metrics: Metrics;
  onClick: () => void;
}

export default function AnalysisCard({
  title,
  description,
  icon,
  color,
  metrics,
  onClick,
}: AnalysisCardProps) {
  const total = metrics.completed + metrics.inProgress;
  const percentage = Math.round((metrics.completed / total) * 100);

  return (
    <Card
      hoverable
      onClick={onClick}
      className="h-full"
    >
      <div className="flex items-start mb-4">
        <div
          className="p-2 rounded-lg mr-3"
          style={{ backgroundColor: `${color}20` }}
        >
          <span style={{ color }}>{icon}</span>
        </div>
        <div>
          <h3 className="text-lg font-semibold">{title}</h3>
          <p className="text-gray-600 text-sm">{description}</p>
        </div>
      </div>
      
      <div className="mt-4">
        <div className="flex justify-between mb-2">
          <span className="text-sm text-gray-600">Progress</span>
          <span className="text-sm font-medium">{percentage}%</span>
        </div>
        <Progress 
          percent={percentage} 
          strokeColor={color}
          showInfo={false}
        />
        <div className="mt-2 flex justify-between text-sm">
          <span className="text-gray-600">
            {metrics.completed} Completed
          </span>
          <span className="text-gray-600">
            {metrics.inProgress} In Progress
          </span>
        </div>
      </div>
    </Card>
  );
} 
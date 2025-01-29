"use client";

import React from 'react';
import { Card, Progress, Tooltip, Divider } from 'antd';
import { ThunderboltOutlined, DropboxOutlined, ExperimentOutlined } from '@ant-design/icons';
import { formatNumber } from '@/lib/formatters';

interface EmissionsBreakdownProps {
  impactAssessment: {
    gwp: number;
    hct: number;
    frs: number;
  };
  processType: string;
}

const EmissionsBreakdown: React.FC<EmissionsBreakdownProps> = ({ 
  impactAssessment,
  processType 
}) => {
  const metrics = [
    {
      key: 'gwp',
      label: 'Global Warming Potential',
      value: impactAssessment.gwp,
      icon: <ThunderboltOutlined />,
      color: '#1890ff',
      unit: 'kg CO₂eq',
      description: 'Carbon dioxide equivalent emissions'
    },
    {
      key: 'hct',
      label: 'Human Carcinogenic Toxicity',
      value: impactAssessment.hct,
      icon: <ExperimentOutlined />,
      color: '#722ed1',
      unit: 'CTUh',
      description: 'Comparative Toxic Units for human health'
    },
    {
      key: 'frs',
      label: 'Fossil Resource Scarcity',
      value: impactAssessment.frs,
      icon: <DropboxOutlined />,
      color: '#13c2c2',
      unit: 'kg oil eq',
      description: 'Oil equivalent of fossil resources used'
    }
  ];

  const totalImpact = Object.values(impactAssessment).reduce((a, b) => a + b, 0);

  return (
    <Card 
      title="Environmental Impact Assessment" 
      className="h-full"
      extra={
        <Tooltip title="Process type">
          <span className="text-sm text-gray-500">{processType.toUpperCase()}</span>
        </Tooltip>
      }
    >
      {metrics.map(metric => {
        const percentage = (metric.value / totalImpact) * 100;
        return (
          <div key={metric.key} className="mb-4">
            <Tooltip title={metric.description}>
              <div className="flex justify-between mb-1">
                <span className="flex items-center">
                  {metric.icon} <span className="ml-2">{metric.label}</span>
                </span>
                <span className="font-medium">
                  {formatNumber(metric.value)} {metric.unit}
                </span>
              </div>
              <Progress
                percent={percentage}
                strokeColor={metric.color}
                showInfo={false}
                strokeWidth={8}
                className="custom-progress"
              />
            </Tooltip>
          </div>
        );
      })}
      
      <Divider className="my-4" />
      
      <div className="text-center">
        <Tooltip title="Total environmental impact score">
          <div className="text-lg font-medium">
            Total Impact Score
          </div>
          <div className="text-3xl font-bold text-primary-600">
            {formatNumber(totalImpact)}
          </div>
        </Tooltip>
      </div>
    </Card>
  );
};

export default EmissionsBreakdown; 
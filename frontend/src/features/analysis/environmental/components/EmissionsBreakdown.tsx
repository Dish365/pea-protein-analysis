"use client";

import React from 'react';
import { Card, Progress, Tooltip } from 'antd';
import { ThunderboltOutlined, WaterOutlined, CarOutlined, DeleteOutlined } from '@ant-design/icons';

interface EmissionsBreakdownProps {
  emissions: {
    electricity: number;
    water: number;
    transport: number;
    waste: number;
    total: number;
  };
}

const EmissionsBreakdown: React.FC<EmissionsBreakdownProps> = ({ emissions }) => {
  const emissionSources = [
    {
      key: 'electricity',
      label: 'Electricity',
      value: emissions.electricity,
      icon: <ThunderboltOutlined />,
      color: '#1890ff',
      unit: 'kg CO₂e',
    },
    {
      key: 'water',
      label: 'Water Usage',
      value: emissions.water,
      icon: <WaterOutlined />,
      color: '#13c2c2',
      unit: 'kg CO₂e',
    },
    {
      key: 'transport',
      label: 'Transportation',
      value: emissions.transport,
      icon: <CarOutlined />,
      color: '#722ed1',
      unit: 'kg CO₂e',
    },
    {
      key: 'waste',
      label: 'Waste Management',
      value: emissions.waste,
      icon: <DeleteOutlined />,
      color: '#eb2f96',
      unit: 'kg CO₂e',
    },
  ];

  return (
    <Card title="Carbon Emissions Breakdown" className="h-full">
      {emissionSources.map(source => {
        const percentage = (source.value / emissions.total) * 100;
        return (
          <div key={source.key} className="mb-4">
            <Tooltip title={`${source.value.toFixed(2)} ${source.unit}`}>
              <div className="flex justify-between mb-1">
                <span>
                  {source.icon} {source.label}
                </span>
                <span>{percentage.toFixed(1)}%</span>
              </div>
              <Progress
                percent={percentage}
                strokeColor={source.color}
                showInfo={false}
              />
            </Tooltip>
          </div>
        );
      })}
      <div className="mt-6 pt-4 border-t">
        <div className="flex justify-between">
          <span className="font-semibold">Total Emissions</span>
          <span className="font-semibold">
            {emissions.total.toFixed(2)} kg CO₂e
          </span>
        </div>
      </div>
    </Card>
  );
};

export default EmissionsBreakdown; 
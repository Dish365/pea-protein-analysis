"use client";

import React from 'react';
import { Card, Row, Col, Statistic, Progress } from 'antd';
import { EnvironmentalResults } from '@/types/environmental';
import { formatNumber } from '@/lib/formatters';

interface EnvironmentalAnalysisViewProps {
  data: EnvironmentalResults;
}

export default function EnvironmentalAnalysisView({ data }: EnvironmentalAnalysisViewProps) {
  return (
    <div className="space-y-6">
      {/* Key Metrics */}
      <Row gutter={[16, 16]}>
        <Col xs={24} md={8}>
          <Card>
            <Statistic
              title="Carbon Footprint"
              value={data.carbonFootprint}
              suffix="kg CO₂e"
              precision={2}
            />
          </Card>
        </Col>
        <Col xs={24} md={8}>
          <Card>
            <Statistic
              title="Water Footprint"
              value={data.waterFootprint}
              suffix="m³"
              precision={2}
            />
          </Card>
        </Col>
        <Col xs={24} md={8}>
          <Card>
            <Statistic
              title="Energy Efficiency"
              value={data.energyEfficiency}
              suffix="%"
              precision={1}
            />
          </Card>
        </Col>
      </Row>

      {/* Emissions Breakdown */}
      <Card title="Emissions Breakdown">
        <div className="space-y-4">
          {Object.entries(data.emissionsBreakdown).map(([source, value]) => (
            <div key={source}>
              <div className="flex justify-between mb-1">
                <span className="capitalize">{source}</span>
                <span>{formatNumber(value)} kg CO₂e</span>
              </div>
              <Progress 
                percent={Math.round((value / data.carbonFootprint) * 100)} 
                showInfo={false}
              />
            </div>
          ))}
        </div>
      </Card>

      {/* Resource Consumption */}
      <Card title="Resource Consumption">
        <Row gutter={[16, 16]}>
          {Object.entries(data.resourceConsumption).map(([resource, value]) => (
            <Col xs={24} sm={12} key={resource}>
              <Statistic
                title={resource.replace(/([A-Z])/g, ' $1').trim()}
                value={value}
                suffix={getResourceUnit(resource)}
                precision={2}
              />
            </Col>
          ))}
        </Row>
      </Card>

      {/* Waste Management */}
      <Card title="Waste Management">
        <Row gutter={[16, 16]}>
          <Col span={24}>
            <div className="text-center mb-4">
              <div className="text-lg font-medium mb-2">
                Waste Recycling Rate
              </div>
              <Progress
                type="circle"
                percent={Math.round(data.wasteRecyclingRate * 100)}
                format={percent => `${percent}%`}
              />
            </div>
          </Col>
        </Row>
      </Card>
    </div>
  );
}

function getResourceUnit(resource: string): string {
  const units: Record<string, string> = {
    water: 'm³',
    electricity: 'kWh',
    naturalGas: 'm³',
    compressedAir: 'm³',
  };
  return units[resource] || '';
} 
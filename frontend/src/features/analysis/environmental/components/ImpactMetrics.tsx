"use client";

import React from 'react';
import { Card, Row, Col, Tooltip } from 'antd';
import { Area } from '@ant-design/plots';

interface ImpactMetricsProps {
  impacts: {
    carbonFootprint: number;
    waterFootprint: number;
    energyIntensity: number;
    wasteIntensity: number;
  };
}

const ImpactMetrics: React.FC<ImpactMetricsProps> = ({ impacts }) => {
  const data = [
    {
      category: 'Carbon Footprint',
      value: impacts.carbonFootprint,
      unit: 'kg CO₂e',
      benchmark: 100, // Example benchmark values
    },
    {
      category: 'Water Footprint',
      value: impacts.waterFootprint,
      unit: 'm³',
      benchmark: 50,
    },
    {
      category: 'Energy Intensity',
      value: impacts.energyIntensity,
      unit: 'kWh/kg',
      benchmark: 5,
    },
    {
      category: 'Waste Intensity',
      value: impacts.wasteIntensity,
      unit: 'kg/kg',
      benchmark: 0.2,
    },
  ];

  const config = {
    data,
    xField: 'category',
    yField: 'value',
    seriesField: 'category',
    color: ['#1890ff', '#13c2c2', '#722ed1', '#eb2f96'],
    legend: false,
    areaStyle: {
      fillOpacity: 0.6,
    },
  };

  return (
    <Card title="Environmental Impact Metrics" className="h-full">
      <Row gutter={[16, 16]}>
        {data.map((item) => (
          <Col xs={12} key={item.category}>
            <Tooltip title={`Benchmark: ${item.benchmark} ${item.unit}`}>
              <div className="text-center mb-4">
                <div className="text-lg font-semibold">{item.category}</div>
                <div className="text-2xl text-primary-600">
                  {item.value.toFixed(2)} {item.unit}
                </div>
                <div className="text-sm text-gray-500">
                  {((item.value / item.benchmark) * 100).toFixed(1)}% of benchmark
                </div>
              </div>
            </Tooltip>
          </Col>
        ))}
      </Row>
      <div className="mt-4 h-64">
        <Area {...config} />
      </div>
    </Card>
  );
};

export default ImpactMetrics; 
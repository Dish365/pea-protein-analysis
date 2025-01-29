"use client";

import React from 'react';
import { Card, Row, Col, Tooltip, Table } from 'antd';
import { Area } from '@ant-design/plots';
import { formatNumber } from '@/lib/formatters';

interface ImpactMetricsProps {
  impacts: {
    gwp: number;
    hct: number;
    frs: number;
  };
  allocatedImpacts: {
    method: string;
    factors: Record<string, number>;
    results: Record<string, Record<string, number>>;
  };
}

const ImpactMetrics: React.FC<ImpactMetricsProps> = ({ impacts, allocatedImpacts }) => {
  const impactMetrics = [
    {
      key: 'gwp',
      name: 'Global Warming Potential',
      value: impacts.gwp,
      unit: 'kg CO₂eq',
      description: 'Carbon dioxide equivalent emissions',
      benchmark: 100 // Example benchmark
    },
    {
      key: 'hct',
      name: 'Human Carcinogenic Toxicity',
      value: impacts.hct,
      unit: 'CTUh',
      description: 'Comparative Toxic Units for human health',
      benchmark: 0.1
    },
    {
      key: 'frs',
      name: 'Fossil Resource Scarcity',
      value: impacts.frs,
      unit: 'kg oil eq',
      description: 'Oil equivalent of fossil resources used',
      benchmark: 50
    }
  ];

  // Prepare data for Area chart
  const chartData = impactMetrics.map(metric => ({
    category: metric.name,
    value: (metric.value / metric.benchmark) * 100,
    actual: metric.value,
    benchmark: metric.benchmark,
    unit: metric.unit
  }));

  const areaConfig = {
    data: chartData,
    xField: 'category',
    yField: 'value',
    seriesField: 'category',
    color: ['#1890ff', '#13c2c2', '#722ed1'],
    legend: { position: 'top' },
    areaStyle: { fillOpacity: 0.6 },
    tooltip: {
      formatter: (datum: any) => ({
        name: datum.category,
        value: `${formatNumber(datum.actual)} ${datum.unit} (${formatNumber(datum.value)}% of benchmark)`
      })
    }
  };

  // Prepare allocation data for table
  const allocationColumns = [
    {
      title: 'Product',
      dataIndex: 'product',
      key: 'product'
    },
    ...impactMetrics.map(metric => ({
      title: metric.name,
      dataIndex: metric.key,
      key: metric.key,
      render: (value: number) => `${formatNumber(value)} ${metric.unit}`
    }))
  ];

  const allocationData = Object.entries(allocatedImpacts.results).map(([product, impacts]) => ({
    key: product,
    product,
    ...impacts
  }));

  return (
    <Card 
      title="Environmental Impact Analysis" 
      className="h-full"
      extra={
        <Tooltip title="Allocation method">
          <span className="text-sm text-gray-500">
            {allocatedImpacts.method.toUpperCase()}
          </span>
        </Tooltip>
      }
    >
      <div className="mb-6">
        <h4 className="text-base mb-2">Impact Metrics vs Benchmarks</h4>
        <div className="h-64">
          <Area {...areaConfig} />
        </div>
      </div>

      <div className="mt-6">
        <h4 className="text-base mb-2">Allocated Impacts by Product</h4>
        <Table 
          columns={allocationColumns} 
          dataSource={allocationData}
          size="small"
          pagination={false}
          scroll={{ x: true }}
        />
      </div>
    </Card>
  );
};

export default ImpactMetrics; 
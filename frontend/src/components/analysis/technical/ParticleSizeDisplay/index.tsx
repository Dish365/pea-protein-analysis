"use client";

import React from 'react';
import { Card, Table, Tooltip, Tag } from 'antd';
import { QuestionCircleOutlined } from '@ant-design/icons';

interface ParticleSizeData {
  distribution: {
    size: number;
    frequency: number;
    cumulative: number;
  }[];
  metrics: {
    d10: number;
    d50: number;
    d90: number;
    meanSize: number;
    standardDev: number;
  };
  targetRange: {
    min: number;
    max: number;
  };
}

interface ParticleSizeDisplayProps {
  d10: number;
  d50: number;
  d90: number;
}

const ParticleSizeDisplay: React.FC<ParticleSizeDisplayProps> = ({
  d10,
  d50,
  d90,
}) => {
  const calculateSpan = () => {
    return (d90 - d10) / d50;
  };

  const getDistributionQuality = (span: number) => {
    if (span <= 1.5) return { text: 'Excellent', color: 'success' };
    if (span <= 2.0) return { text: 'Good', color: 'processing' };
    if (span <= 2.5) return { text: 'Fair', color: 'warning' };
    return { text: 'Poor', color: 'error' };
  };

  const span = calculateSpan();
  const quality = getDistributionQuality(span);

  const columns = [
    {
      title: 'Metric',
      dataIndex: 'metric',
      key: 'metric',
      render: (text: string, record: any) => (
        <span>
          {text}
          {record.tooltip && (
            <Tooltip title={record.tooltip}>
              <QuestionCircleOutlined style={{ marginLeft: 8 }} />
            </Tooltip>
          )}
        </span>
      ),
    },
    {
      title: 'Value',
      dataIndex: 'value',
      key: 'value',
      render: (value: any) => {
        if (typeof value === 'number') {
          return `${value.toFixed(1)} μm`;
        }
        return value;
      },
    },
    {
      title: 'Status',
      dataIndex: 'status',
      key: 'status',
      render: (status: any) => {
        if (!status) return null;
        return <Tag color={status.color}>{status.text}</Tag>;
      },
    },
  ];

  const data = [
    {
      key: '1',
      metric: 'D10 (Fine Particles)',
      value: d10,
      tooltip: '10% of particles are smaller than this size',
    },
    {
      key: '2',
      metric: 'D50 (Median Size)',
      value: d50,
      tooltip: 'Median particle size (50% are smaller/larger)',
    },
    {
      key: '3',
      metric: 'D90 (Coarse Particles)',
      value: d90,
      tooltip: '90% of particles are smaller than this size',
    },
    {
      key: '4',
      metric: 'Distribution Span',
      value: span.toFixed(2),
      status: quality,
      tooltip: 'Measure of distribution width (D90-D10)/D50',
    },
  ];

  return (
    <Card 
      title="Particle Size Distribution" 
      className="particle-size-card"
      extra={
        <Tooltip title="Overall distribution quality">
          <Tag color={quality.color}>{quality.text} Distribution</Tag>
        </Tooltip>
      }
    >
      <Table 
        columns={columns} 
        dataSource={data} 
        pagination={false}
        className="particle-size-table"
      />
    </Card>
  );
};

export default ParticleSizeDisplay;

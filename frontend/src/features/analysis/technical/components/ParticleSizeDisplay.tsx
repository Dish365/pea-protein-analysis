"use client";

import React from 'react';
import { Card, Table, Tooltip, Tag } from 'antd';
import { QuestionCircleOutlined } from '@ant-design/icons';
import { ColumnsType } from 'antd/es/table';

interface ParticleSizeDisplayProps {
  d10: number;
  d50: number;
  d90: number;
  span: number;
}

interface DataType {
  key: string;
  metric: string;
  value: number;
  tooltip?: string;
  status?: {
    text: string;
    color: string;
  };
}

const ParticleSizeDisplay: React.FC<ParticleSizeDisplayProps> = ({
  d10,
  d50,
  d90,
  span,
}) => {
  const getDistributionQuality = (span: number) => {
    if (span <= 1.5) return { text: 'Excellent', color: 'success' };
    if (span <= 2.0) return { text: 'Good', color: 'processing' };
    if (span <= 2.5) return { text: 'Fair', color: 'warning' };
    return { text: 'Poor', color: 'error' };
  };

  const quality = getDistributionQuality(span);

  const columns: ColumnsType<DataType> = [
    {
      title: 'Metric',
      dataIndex: 'metric',
      key: 'metric',
      render: (text: string, record) => (
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
      render: (value: number) => `${value.toFixed(1)} μm`,
    },
    {
      title: 'Status',
      dataIndex: 'status',
      key: 'status',
      render: (status?: { text: string; color: string }) => {
        if (!status) return null;
        return <Tag color={status.color}>{status.text}</Tag>;
      },
    },
  ];

  const data: DataType[] = [
    {
      key: 'd10',
      metric: 'D10 (Fine Particles)',
      value: d10,
      tooltip: '10% of particles are smaller than this size',
    },
    {
      key: 'd50',
      metric: 'D50 (Median Size)',
      value: d50,
      tooltip: 'Median particle size (50% are smaller/larger)',
    },
    {
      key: 'd90',
      metric: 'D90 (Coarse Particles)',
      value: d90,
      tooltip: '90% of particles are smaller than this size',
    },
    {
      key: 'span',
      metric: 'Distribution Span',
      value: span,
      tooltip: 'Measure of distribution width (D90-D10)/D50',
      status: quality,
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
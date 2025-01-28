"use client";

import React from 'react';
import { Card, Table, Tag, Tooltip } from 'antd';
import { InfoCircleOutlined } from '@ant-design/icons';
import { formatCurrency } from '@/lib/formatters';

interface SensitivityData {
  parameter: string;
  baseValue: number;
  impact: number;
  sensitivity: 'Low' | 'Medium' | 'High';
}

interface SensitivityAnalysisProps {
  sensitivityData: SensitivityData[];
}

const SensitivityAnalysis: React.FC<SensitivityAnalysisProps> = ({
  sensitivityData,
}) => {
  const columns = [
    {
      title: 'Parameter',
      dataIndex: 'parameter',
      key: 'parameter',
      render: (text: string) => (
        <span>
          {text}
          <Tooltip title={`Impact of changes in ${text.toLowerCase()} on profitability`}>
            <InfoCircleOutlined style={{ marginLeft: 8 }} />
          </Tooltip>
        </span>
      ),
    },
    {
      title: 'Base Value',
      dataIndex: 'baseValue',
      key: 'baseValue',
      render: (value: number) => formatCurrency(value),
    },
    {
      title: 'Impact on Profitability',
      dataIndex: 'impact',
      key: 'impact',
      render: (impact: number) => (
        <span>
          {impact >= 0 ? '+' : ''}{impact.toFixed(1)}%
        </span>
      ),
    },
    {
      title: 'Sensitivity',
      dataIndex: 'sensitivity',
      key: 'sensitivity',
      render: (sensitivity: string) => {
        const color = 
          sensitivity === 'High' ? 'red' :
          sensitivity === 'Medium' ? 'orange' : 'green';
        return <Tag color={color}>{sensitivity}</Tag>;
      },
    },
  ];

  return (
    <Card 
      title="Sensitivity Analysis" 
      className="sensitivity-analysis-card"
      extra={
        <Tooltip title="Analysis of how changes in parameters affect profitability">
          <InfoCircleOutlined />
        </Tooltip>
      }
    >
      <Table 
        columns={columns}
        dataSource={sensitivityData}
        pagination={false}
      />
    </Card>
  );
};

export default SensitivityAnalysis; 
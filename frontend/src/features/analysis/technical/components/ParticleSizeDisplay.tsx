"use client";

import React from 'react';
import { Card, Table, Tooltip, Tag, Row, Col, Statistic } from 'antd';
import { QuestionCircleOutlined, DotChartOutlined, ColumnHeightOutlined, BarChartOutlined } from '@ant-design/icons';
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
  tooltip: string;
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

  const getParticleRange = (d10: number, d90: number) => {
    const range = d90 - d10;
    if (range <= 50) return { text: 'Narrow', color: 'success' };
    if (range <= 100) return { text: 'Moderate', color: 'processing' };
    if (range <= 150) return { text: 'Wide', color: 'warning' };
    return { text: 'Very Wide', color: 'error' };
  };

  const quality = getDistributionQuality(span);
  const range = getParticleRange(d10, d90);

  const columns: ColumnsType<DataType> = [
    {
      title: 'Metric',
      dataIndex: 'metric',
      key: 'metric',
      render: (text: string, record) => (
        <span>
          {text}
          <Tooltip title={record.tooltip}>
            <QuestionCircleOutlined style={{ marginLeft: 8 }} />
          </Tooltip>
        </span>
      ),
    },
    {
      title: 'Value',
      dataIndex: 'value',
      key: 'value',
      align: 'right',
      render: (value: number) => `${value.toFixed(1)} μm`,
    },
    {
      title: 'Status',
      dataIndex: 'status',
      key: 'status',
      align: 'center',
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
        <Row gutter={16} align="middle">
          <Col>
            <Tooltip title="Distribution quality">
              <Tag color={quality.color} icon={<BarChartOutlined />}>
                {quality.text} Distribution
              </Tag>
            </Tooltip>
          </Col>
          <Col>
            <Tooltip title="Size range">
              <Tag color={range.color} icon={<ColumnHeightOutlined />}>
                {range.text} Range
              </Tag>
            </Tooltip>
          </Col>
        </Row>
      }
    >
      <Row gutter={[16, 16]}>
        <Col xs={24} lg={16}>
          <Table 
            columns={columns} 
            dataSource={data} 
            pagination={false}
            size="small"
            className="particle-size-table"
          />
        </Col>
        <Col xs={24} lg={8}>
          <Card className="summary-card">
            <Statistic
              title={
                <span>
                  Size Distribution Score
                  <Tooltip title="Overall quality score based on span and range">
                    <QuestionCircleOutlined style={{ marginLeft: 8 }} />
                  </Tooltip>
                </span>
              }
              value={Math.max(0, 100 - (span * 20))}
              suffix="%"
              prefix={<DotChartOutlined />}
              valueStyle={{ 
                color: quality.color === 'success' ? '#3f8600' : 
                       quality.color === 'processing' ? '#1890ff' :
                       quality.color === 'warning' ? '#faad14' : '#cf1322',
                fontSize: '1.5rem'
              }}
            />
            <div className="mt-4">
              <Tooltip title="Ideal range: D90-D10 < 100μm">
                <Tag color={range.color}>Range: {(d90 - d10).toFixed(1)} μm</Tag>
              </Tooltip>
            </div>
          </Card>
        </Col>
      </Row>
    </Card>
  );
};

export default ParticleSizeDisplay; 
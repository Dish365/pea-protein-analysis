"use client";

import React from 'react';
import { Card, Statistic, Row, Col, Tooltip, Progress } from 'antd';
import { 
  ThunderboltOutlined, 
  DropboxOutlined,
  ExperimentOutlined
} from '@ant-design/icons';
import { formatNumber } from '@/lib/formatters';

interface ResourceConsumptionProps {
  consumptionMetrics: {
    electricity: number | null;
    cooling: number | null;
    water: number | null;
  };
  processType: string;
}

const ResourceConsumption: React.FC<ResourceConsumptionProps> = ({ 
  consumptionMetrics,
  processType 
}) => {
  const metrics = [
    {
      key: 'electricity',
      title: 'Electricity Consumption',
      value: consumptionMetrics.electricity,
      suffix: 'kWh',
      icon: <ThunderboltOutlined />,
      tooltip: 'Total electrical energy consumed',
      color: '#1890ff',
      visible: processType === 'rf'
    },
    {
      key: 'cooling',
      title: 'Cooling Energy',
      value: consumptionMetrics.cooling,
      suffix: 'kWh',
      icon: <ExperimentOutlined />,
      tooltip: 'Total cooling energy required',
      color: '#13c2c2',
      visible: processType === 'ir'
    },
    {
      key: 'water',
      title: 'Water Usage',
      value: consumptionMetrics.water,
      suffix: 'm³',
      icon: <DropboxOutlined />,
      tooltip: 'Total water consumption',
      color: '#52c41a',
      visible: true
    }
  ].filter(metric => metric.visible);

  return (
    <Card 
      title="Resource Consumption" 
      className="h-full"
      extra={
        <Tooltip title="Process specific consumption">
          <span className="text-sm text-gray-500">{processType.toUpperCase()}</span>
        </Tooltip>
      }
    >
      <Row gutter={[16, 16]}>
        {metrics.map(metric => (
          <Col xs={24} sm={12} key={metric.key}>
            <Tooltip title={metric.tooltip}>
              <Card className="resource-metric-card">
                <Statistic
                  title={
                    <span className="flex items-center">
                      {metric.icon}
                      <span className="ml-2">{metric.title}</span>
                    </span>
                  }
                  value={metric.value !== null ? formatNumber(metric.value) : 'N/A'}
                  suffix={metric.value !== null ? metric.suffix : ''}
                  valueStyle={{ color: metric.color }}
                />
                {metric.value !== null && (
                  <Progress 
                    percent={75} // You can calculate this based on benchmarks
                    strokeColor={metric.color}
                    showInfo={false}
                    size="small"
                    className="mt-2"
                  />
                )}
              </Card>
            </Tooltip>
          </Col>
        ))}
      </Row>
    </Card>
  );
};

export default ResourceConsumption; 
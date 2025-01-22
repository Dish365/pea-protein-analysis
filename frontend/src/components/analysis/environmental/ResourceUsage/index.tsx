"use client";

import React from 'react';
import { Card, Statistic, Row, Col, Progress, Tooltip } from 'antd';
import { 
  ThunderboltOutlined,
  ExperimentOutlined,
  DeploymentUnitOutlined,
  RocketOutlined
} from '@ant-design/icons';
import { ProcessType } from '../../../../types/process';

interface ResourceMetrics {
  electricity: { consumption: number; perKg: number };
  cooling: { consumption: number; perKg: number };
  water: { consumption: number; perKg: number };
  transport: { consumption: number; perKg: number };
}

interface ResourceUsageProps {
  resourceMetrics: ResourceMetrics;
  productionVolume: number;
  processType: ProcessType;
}

export const ResourceUsage: React.FC<ResourceUsageProps> = ({
  resourceMetrics,
  productionVolume,
  processType,
}) => {
  const resources = [
    {
      title: 'Electricity Usage',
      consumption: resourceMetrics.electricity.consumption,
      perKg: resourceMetrics.electricity.perKg,
      unit: 'kWh',
      icon: <ThunderboltOutlined />,
      color: '#faad14',
      tooltip: 'Total electricity consumption and per kg of product',
      threshold: processType === ProcessType.RF ? 200 : 150,
    },
    {
      title: 'Cooling Energy',
      consumption: resourceMetrics.cooling.consumption,
      perKg: resourceMetrics.cooling.perKg,
      unit: 'kWh',
      icon: <ExperimentOutlined />,
      color: '#1890ff',
      tooltip: 'Total cooling energy consumption and per kg of product',
      threshold: processType === ProcessType.IR ? 60 : 40,
    },
    {
      title: 'Water Usage',
      consumption: resourceMetrics.water.consumption,
      perKg: resourceMetrics.water.perKg,
      unit: 'kg',
      icon: <DeploymentUnitOutlined />,
      color: '#52c41a',
      tooltip: 'Total water consumption and per kg of product',
      threshold: 250,
    },
    {
      title: 'Transport Energy',
      consumption: resourceMetrics.transport.consumption,
      perKg: resourceMetrics.transport.perKg,
      unit: 'MJ',
      icon: <RocketOutlined />,
      color: '#722ed1',
      tooltip: 'Total transport energy consumption and per kg of product',
      threshold: 120,
    },
  ];

  return (
    <Card title="Resource Usage Analysis" className="resource-usage-card">
      {resources.map((resource, index) => (
        <div key={index} className="resource-metric" style={{ marginBottom: index < resources.length - 1 ? '24px' : 0 }}>
          <Tooltip title={resource.tooltip}>
            <Card className="metric-card">
              <Row gutter={[16, 16]}>
                <Col xs={24} sm={12}>
                  <Statistic
                    title={`Total ${resource.title}`}
                    value={resource.consumption}
                    precision={1}
                    prefix={resource.icon}
                    suffix={resource.unit}
                  />
                  <Progress
                    percent={(resource.consumption / resource.threshold) * 100}
                    status={(resource.consumption / resource.threshold) <= 1 ? 'success' : 'exception'}
                    strokeColor={resource.color}
                  />
                </Col>
                <Col xs={24} sm={12}>
                  <Statistic
                    title={`${resource.title} per kg`}
                    value={resource.perKg}
                    precision={2}
                    prefix={resource.icon}
                    suffix={`${resource.unit}/kg`}
                  />
                  <Progress
                    percent={(resource.perKg / (resource.threshold / productionVolume)) * 100}
                    status={(resource.perKg / (resource.threshold / productionVolume)) <= 1 ? 'success' : 'exception'}
                    strokeColor={resource.color}
                  />
                </Col>
              </Row>
            </Card>
          </Tooltip>
        </div>
      ))}
    </Card>
  );
};

export default ResourceUsage;

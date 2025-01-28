"use client";

import React from 'react';
import { Card, Statistic, Row, Col, Tooltip } from 'antd';
import { 
  ThunderboltOutlined, 
  WaterOutlined,
  ReconciliationOutlined,
  DeleteOutlined 
} from '@ant-design/icons';

interface ResourceConsumptionProps {
  resources: {
    energyConsumption: number;
    waterConsumption: number;
    materialEfficiency: number;
    wasteGeneration: number;
  };
}

const ResourceConsumption: React.FC<ResourceConsumptionProps> = ({ resources }) => {
  const metrics = [
    {
      key: 'energy',
      title: 'Energy Consumption',
      value: resources.energyConsumption,
      suffix: 'kWh',
      icon: <ThunderboltOutlined />,
      tooltip: 'Total energy consumed in the process',
      color: '#1890ff',
    },
    {
      key: 'water',
      title: 'Water Consumption',
      value: resources.waterConsumption,
      suffix: 'm³',
      icon: <WaterOutlined />,
      tooltip: 'Total water used in the process',
      color: '#13c2c2',
    },
    {
      key: 'efficiency',
      title: 'Material Efficiency',
      value: resources.materialEfficiency,
      suffix: '%',
      icon: <ReconciliationOutlined />,
      tooltip: 'Percentage of input material effectively used',
      color: '#52c41a',
    },
    {
      key: 'waste',
      title: 'Waste Generation',
      value: resources.wasteGeneration,
      suffix: 'kg',
      icon: <DeleteOutlined />,
      tooltip: 'Total waste generated during the process',
      color: '#eb2f96',
    },
  ];

  return (
    <Card title="Resource Consumption" className="h-full">
      <Row gutter={[16, 16]}>
        {metrics.map(metric => (
          <Col xs={12} key={metric.key}>
            <Tooltip title={metric.tooltip}>
              <Card className="metric-card">
                <Statistic
                  title={metric.title}
                  value={metric.value}
                  precision={2}
                  suffix={metric.suffix}
                  prefix={metric.icon}
                  valueStyle={{ color: metric.color }}
                />
              </Card>
            </Tooltip>
          </Col>
        ))}
      </Row>
    </Card>
  );
};

export default ResourceConsumption; 
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

interface EcoEfficiencyMetrics {
  energyEfficiency: number;
  waterEfficiency: number;
  materialEfficiency: number;
  transportEfficiency: number;
}

interface EcoEfficiencyDisplayProps {
  ecoEfficiency: EcoEfficiencyMetrics;
  processType: ProcessType;
  productionVolume: number;
}

export const EcoEfficiencyDisplay: React.FC<EcoEfficiencyDisplayProps> = ({
  ecoEfficiency,
  processType,
  productionVolume,
}) => {
  const metrics = [
    {
      title: 'Energy Efficiency',
      value: ecoEfficiency.energyEfficiency,
      icon: <ThunderboltOutlined />,
      color: '#faad14',
      tooltip: 'Ratio of theoretical to actual energy consumption',
      threshold: processType === ProcessType.RF ? 85 : 80,
      unit: '%',
    },
    {
      title: 'Water Efficiency',
      value: ecoEfficiency.waterEfficiency,
      icon: <ExperimentOutlined />,
      color: '#1890ff',
      tooltip: 'Production output per unit of water consumption',
      threshold: 4.0, // kg product per kg water
      unit: 'kg/kg',
    },
    {
      title: 'Material Efficiency',
      value: ecoEfficiency.materialEfficiency * 100,
      icon: <DeploymentUnitOutlined />,
      color: '#52c41a',
      tooltip: 'Output to input mass ratio',
      threshold: 90,
      unit: '%',
    },
    {
      title: 'Transport Efficiency',
      value: ecoEfficiency.transportEfficiency,
      icon: <RocketOutlined />,
      color: '#722ed1',
      tooltip: 'Production output per unit of transport energy',
      threshold: 8.0, // kg product per MJ transport
      unit: 'kg/MJ',
    },
  ];

  return (
    <Card 
      title="Eco-Efficiency Analysis" 
      className="eco-efficiency-card"
      extra={
        <Tooltip title="Higher values indicate better environmental performance">
          <span>Performance Metrics</span>
        </Tooltip>
      }
    >
      <Row gutter={[16, 16]}>
        {metrics.map((metric, index) => (
          <Col xs={24} sm={12} key={index}>
            <Tooltip title={metric.tooltip}>
              <Card className="metric-card">
                <Statistic
                  title={metric.title}
                  value={metric.value}
                  precision={2}
                  prefix={metric.icon}
                  suffix={metric.unit}
                  valueStyle={{ 
                    color: metric.value >= metric.threshold ? '#3f8600' : '#cf1322'
                  }}
                />
                <Progress
                  percent={(metric.value / metric.threshold) * 100}
                  status={(metric.value / metric.threshold) >= 1 ? 'success' : 'normal'}
                  strokeColor={metric.color}
                />
                <div className="metric-benchmark" style={{ fontSize: '12px', marginTop: '8px' }}>
                  Benchmark: {metric.threshold} {metric.unit}
                </div>
              </Card>
            </Tooltip>
          </Col>
        ))}
      </Row>

      <div className="process-info" style={{ marginTop: '16px' }}>
        <Card size="small">
          <Row gutter={16}>
            <Col span={12}>
              <Statistic
                title="Process Type"
                value={processType}
                valueStyle={{ fontSize: '14px' }}
              />
            </Col>
            <Col span={12}>
              <Statistic
                title="Production Volume"
                value={productionVolume}
                suffix="kg/year"
                valueStyle={{ fontSize: '14px' }}
              />
            </Col>
          </Row>
        </Card>
      </div>
    </Card>
  );
};

export default EcoEfficiencyDisplay;

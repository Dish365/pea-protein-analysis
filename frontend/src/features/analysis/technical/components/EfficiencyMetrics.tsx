"use client";

import React from 'react';
import { Card, Statistic, Row, Col, Progress, Tooltip } from 'antd';
import { 
  ThunderboltOutlined, 
  DeploymentUnitOutlined, 
  DashboardOutlined,
  AimOutlined 
} from '@ant-design/icons';

interface EfficiencyMetricsProps {
  massEfficiency: number;
  processEfficiency: number;
  throughputRate: number;
  classifierEfficiency: number;
}

const EfficiencyMetrics: React.FC<EfficiencyMetricsProps> = ({
  massEfficiency,
  processEfficiency,
  throughputRate,
  classifierEfficiency,
}) => {
  const metrics = [
    {
      title: 'Mass Efficiency',
      value: massEfficiency,
      icon: <DeploymentUnitOutlined />,
      suffix: '%',
      tooltip: 'Ratio of output mass to input mass',
      threshold: 85,
    },
    {
      title: 'Process Efficiency',
      value: processEfficiency,
      icon: <ThunderboltOutlined />,
      suffix: '%',
      tooltip: 'Overall process efficiency',
      threshold: 90,
    },
    {
      title: 'Throughput Rate',
      value: throughputRate,
      icon: <DashboardOutlined />,
      suffix: 'kg/h',
      tooltip: 'Material processing rate',
      threshold: 80,
    },
    {
      title: 'Classifier Efficiency',
      value: classifierEfficiency,
      icon: <AimOutlined />,
      suffix: '%',
      tooltip: 'Classifier performance efficiency',
      threshold: 95,
    },
  ];

  return (
    <Card title="Process Efficiency Metrics" className="h-full">
      <Row gutter={[16, 16]}>
        {metrics.map((metric, index) => (
          <Col xs={24} sm={12} key={index}>
            <Tooltip title={metric.tooltip}>
              <Card className="metric-card">
                <Statistic
                  title={metric.title}
                  value={metric.value}
                  precision={1}
                  suffix={metric.suffix}
                  prefix={metric.icon}
                  valueStyle={{ 
                    color: metric.value >= metric.threshold ? '#3f8600' : '#cf1322'
                  }}
                />
                <Progress
                  percent={metric.value}
                  status={metric.value >= metric.threshold ? 'success' : 'normal'}
                  strokeColor={metric.value >= metric.threshold ? '#52c41a' : '#1890ff'}
                />
              </Card>
            </Tooltip>
          </Col>
        ))}
      </Row>
    </Card>
  );
};

export default EfficiencyMetrics; 
"use client";

import React from 'react';
import { Card, Statistic, Row, Col, Progress, Tooltip } from 'antd';
import { 
  ThunderboltOutlined, 
  DeploymentUnitOutlined, 
  FilterOutlined,
  PercentageOutlined 
} from '@ant-design/icons';

interface EfficiencyMetricsProps {
  massEfficiency: number;
  processEfficiency: number;
  separationEfficiency: number;
  proteinYield: number;
}

const EfficiencyMetrics: React.FC<EfficiencyMetricsProps> = ({
  massEfficiency,
  processEfficiency,
  separationEfficiency,
  proteinYield,
}) => {
  const metrics = [
    {
      title: 'Mass Efficiency',
      value: massEfficiency,
      icon: <DeploymentUnitOutlined />,
      suffix: '%',
      tooltip: 'Ratio of recovered mass to input mass',
      threshold: 85,
    },
    {
      title: 'Process Efficiency',
      value: processEfficiency,
      icon: <ThunderboltOutlined />,
      suffix: '%',
      tooltip: 'Overall process performance efficiency',
      threshold: 90,
    },
    {
      title: 'Separation Efficiency',
      value: separationEfficiency,
      icon: <FilterOutlined />,
      suffix: '%',
      tooltip: 'Efficiency of protein separation process',
      threshold: 80,
    },
    {
      title: 'Protein Yield',
      value: proteinYield,
      icon: <PercentageOutlined />,
      suffix: '%',
      tooltip: 'Total protein yield from the process',
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
                    color: metric.value >= metric.threshold ? '#3f8600' : '#cf1322',
                    fontSize: '1.5rem'
                  }}
                />
                <Progress
                  percent={Math.min(100, Math.max(0, metric.value))}
                  status={metric.value >= metric.threshold ? 'success' : 'normal'}
                  strokeColor={metric.value >= metric.threshold ? '#52c41a' : '#1890ff'}
                  size="small"
                  className="mt-2"
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
"use client";

import React from 'react';
import { Card, Statistic, Row, Col, Progress, Tooltip } from 'antd';
import { ExperimentOutlined, PercentageOutlined, ScissorOutlined } from '@ant-design/icons';

interface ProteinRecoveryCardProps {
  massRecovery: number;
  contentRecovery: number;
  yieldRecovery: number;
}

const ProteinRecoveryCard: React.FC<ProteinRecoveryCardProps> = ({
  massRecovery,
  contentRecovery,
  yieldRecovery,
}) => {
  const metrics = [
    {
      title: 'Mass Recovery',
      value: massRecovery,
      icon: <ExperimentOutlined />,
      suffix: '%',
      tooltip: 'Percentage of protein mass recovered',
      threshold: 90,
    },
    {
      title: 'Content Recovery',
      value: contentRecovery,
      icon: <PercentageOutlined />,
      suffix: '%',
      tooltip: 'Protein content in recovered material',
      threshold: 95,
    },
    {
      title: 'Yield Recovery',
      value: yieldRecovery,
      icon: <ScissorOutlined />,
      suffix: '%',
      tooltip: 'Overall protein yield efficiency',
      threshold: 85,
    },
  ];

  return (
    <Card 
      title="Protein Recovery Analysis" 
      className="h-full"
      extra={
        <Tooltip title="Overall recovery performance">
          <span className={`text-${yieldRecovery >= 85 ? 'success' : 'warning'}`}>
            {yieldRecovery >= 85 ? 'Optimal' : 'Suboptimal'}
          </span>
        </Tooltip>
      }
    >
      <Row gutter={[16, 16]}>
        {metrics.map((metric, index) => (
          <Col xs={24} key={index}>
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

export default ProteinRecoveryCard; 
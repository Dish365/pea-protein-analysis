"use client";

import React from 'react';
import { Card, Statistic, Row, Col, Progress, Tooltip } from 'antd';
import { ExperimentOutlined, PercentageOutlined } from '@ant-design/icons';

interface ProteinRecoveryCardProps {
  initialMass: number;
  finalMass: number;
  recoveryRate: number;
  concentrationIncrease: number;
}

const ProteinRecoveryCard: React.FC<ProteinRecoveryCardProps> = ({
  initialMass,
  finalMass,
  recoveryRate,
  concentrationIncrease,
}) => {
  const metrics = [
    {
      title: 'Recovery Rate',
      value: recoveryRate,
      icon: <ExperimentOutlined />,
      suffix: '%',
      tooltip: 'Percentage of initial protein recovered in final product',
      threshold: 90,
    },
    {
      title: 'Concentration Increase',
      value: concentrationIncrease,
      icon: <PercentageOutlined />,
      suffix: '%',
      tooltip: 'Percentage increase in protein concentration',
      threshold: 10,
    },
  ];

  return (
    <Card title="Protein Recovery Analysis" className="h-full">
      <Row gutter={[16, 16]}>
        <Col xs={24} sm={12}>
          <Tooltip title="Total protein mass before processing">
            <Statistic
              title="Initial Protein Mass"
              value={initialMass}
              precision={2}
              suffix="kg"
              prefix={<ExperimentOutlined />}
            />
          </Tooltip>
        </Col>
        <Col xs={24} sm={12}>
          <Tooltip title="Total protein mass after processing">
            <Statistic
              title="Final Protein Mass"
              value={finalMass}
              precision={2}
              suffix="kg"
              prefix={<ExperimentOutlined />}
            />
          </Tooltip>
        </Col>
      </Row>

      <div className="mt-6">
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
                    percent={Math.min(100, Math.max(0, metric.value))}
                    status={metric.value >= metric.threshold ? 'success' : 'normal'}
                    strokeColor={metric.value >= metric.threshold ? '#52c41a' : '#1890ff'}
                  />
                </Card>
              </Tooltip>
            </Col>
          ))}
        </Row>
      </div>
    </Card>
  );
};

export default ProteinRecoveryCard; 
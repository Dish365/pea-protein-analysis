"use client";

import React from 'react';
import { Card, Progress, Row, Col, Tooltip } from 'antd';
import { CheckCircleOutlined, WarningOutlined } from '@ant-design/icons';

interface SustainabilityScoreProps {
  metrics: {
    sustainabilityScore: number;
    circularityIndex: number;
    resourceEfficiency: number;
  };
}

const SustainabilityScore: React.FC<SustainabilityScoreProps> = ({ metrics }) => {
  const getScoreColor = (score: number, type: 'score' | 'circularity' | 'efficiency') => {
    const thresholds = {
      score: { good: 70, medium: 50 },
      circularity: { good: 0.7, medium: 0.5 },
      efficiency: { good: 70, medium: 50 },
    };

    const threshold = thresholds[type];
    if (type === 'circularity') {
      return score >= threshold.good ? '#52c41a' : 
             score >= threshold.medium ? '#faad14' : '#f5222d';
    }
    return score >= threshold.good ? '#52c41a' : 
           score >= threshold.medium ? '#faad14' : '#f5222d';
  };

  return (
    <Card title="Sustainability Assessment" className="h-full">
      <div className="text-center mb-6">
        <Tooltip title="Overall sustainability score based on multiple factors">
          <div className="mb-4">
            <Progress
              type="dashboard"
              percent={metrics.sustainabilityScore}
              strokeColor={getScoreColor(metrics.sustainabilityScore, 'score')}
              format={percent => (
                <div>
                  <div className="text-2xl">{percent}</div>
                  <div className="text-xs">Sustainability Score</div>
                </div>
              )}
            />
          </div>
        </Tooltip>
      </div>

      <Row gutter={[16, 16]}>
        <Col span={12}>
          <Tooltip title="Measure of material circularity in the process">
            <Card className="text-center">
              <Progress
                type="circle"
                percent={metrics.circularityIndex * 100}
                strokeColor={getScoreColor(metrics.circularityIndex, 'circularity')}
                size={80}
              />
              <div className="mt-2">Circularity Index</div>
            </Card>
          </Tooltip>
        </Col>
        <Col span={12}>
          <Tooltip title="Overall resource utilization efficiency">
            <Card className="text-center">
              <Progress
                type="circle"
                percent={metrics.resourceEfficiency}
                strokeColor={getScoreColor(metrics.resourceEfficiency, 'efficiency')}
                size={80}
              />
              <div className="mt-2">Resource Efficiency</div>
            </Card>
          </Tooltip>
        </Col>
      </Row>

      <div className="mt-6">
        <div className="flex items-center mb-2">
          {metrics.sustainabilityScore >= 70 ? (
            <CheckCircleOutlined className="text-success mr-2" />
          ) : (
            <WarningOutlined className="text-warning mr-2" />
          )}
          <span>
            {metrics.sustainabilityScore >= 70
              ? 'Process meets sustainability targets'
              : 'Improvements needed to meet targets'}
          </span>
        </div>
      </div>
    </Card>
  );
};

export default SustainabilityScore; 
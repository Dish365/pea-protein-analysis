"use client";

import React from 'react';
import { Card, Progress, Row, Col, Tooltip, Statistic } from 'antd';
import { CheckCircleOutlined, WarningOutlined } from '@ant-design/icons';
import { formatNumber } from '@/lib/formatters';

interface SustainabilityScoreProps {
  impacts: {
    gwp: number;
    hct: number;
    frs: number;
  };
  processType: string;
}

const SustainabilityScore: React.FC<SustainabilityScoreProps> = ({ 
  impacts,
  processType 
}) => {
  // Calculate sustainability metrics based on impacts
  const calculateMetrics = () => {
    const benchmarks = {
      baseline: { gwp: 100, hct: 0.1, frs: 50 },
      rf: { gwp: 90, hct: 0.08, frs: 45 },
      ir: { gwp: 95, hct: 0.09, frs: 47 }
    };

    const benchmark = benchmarks[processType as keyof typeof benchmarks] || benchmarks.baseline;
    
    // Calculate relative scores (0-100)
    const gwpScore = Math.max(0, 100 * (1 - impacts.gwp / benchmark.gwp));
    const hctScore = Math.max(0, 100 * (1 - impacts.hct / benchmark.hct));
    const frsScore = Math.max(0, 100 * (1 - impacts.frs / benchmark.frs));

    // Calculate overall sustainability score
    const sustainabilityScore = (gwpScore + hctScore + frsScore) / 3;

    // Calculate circularity based on resource efficiency
    const circularityIndex = Math.min(1, Math.max(0, 1 - (impacts.frs / benchmark.frs)));

    // Calculate resource efficiency
    const resourceEfficiency = Math.min(100, Math.max(0, 100 * (1 - impacts.gwp / benchmark.gwp)));

    return {
      sustainabilityScore,
      circularityIndex,
      resourceEfficiency
    };
  };

  const metrics = calculateMetrics();

  const getScoreColor = (score: number) => {
    if (score >= 70) return '#52c41a';
    if (score >= 50) return '#faad14';
    return '#f5222d';
  };

  return (
    <Card 
      title="Sustainability Assessment" 
      className="h-full"
      extra={
        <Tooltip title="Process type">
          <span className="text-sm text-gray-500">{processType.toUpperCase()}</span>
        </Tooltip>
      }
    >
      <div className="text-center mb-6">
        <Tooltip title="Overall sustainability score based on environmental impacts">
          <div className="mb-4">
            <Progress
              type="dashboard"
              percent={Math.round(metrics.sustainabilityScore)}
              strokeColor={getScoreColor(metrics.sustainabilityScore)}
              format={percent => (
                <div>
                  <div className="text-2xl">{formatNumber(percent || 0)}</div>
                  <div className="text-xs">Sustainability Score</div>
                </div>
              )}
            />
          </div>
        </Tooltip>
      </div>

      <Row gutter={[16, 16]}>
        <Col span={12}>
          <Tooltip title="Measure of process circularity">
            <Card className="text-center">
              <Statistic
                title="Circularity Index"
                value={metrics.circularityIndex}
                precision={2}
                valueStyle={{ color: getScoreColor(metrics.circularityIndex * 100) }}
                suffix="/ 1.0"
              />
            </Card>
          </Tooltip>
        </Col>
        <Col span={12}>
          <Tooltip title="Resource utilization efficiency">
            <Card className="text-center">
              <Statistic
                title="Resource Efficiency"
                value={metrics.resourceEfficiency}
                precision={1}
                valueStyle={{ color: getScoreColor(metrics.resourceEfficiency) }}
                suffix="%"
              />
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
              : metrics.sustainabilityScore >= 50
              ? 'Process needs minor improvements'
              : 'Significant improvements needed'}
          </span>
        </div>
      </div>
    </Card>
  );
};

export default SustainabilityScore; 
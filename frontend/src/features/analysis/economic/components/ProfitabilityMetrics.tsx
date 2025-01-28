"use client";

import React from 'react';
import { Card, Statistic, Row, Col, Progress, Tooltip } from 'antd';
import { 
  DollarOutlined, 
  PercentageOutlined,
  FieldTimeOutlined 
} from '@ant-design/icons';
import { formatCurrency } from '@/lib/formatters';

interface ProfitabilityMetricsProps {
  metrics: {
    annualRevenue: number;
    annualProfit: number;
    roi: number;
    paybackPeriod: number;
    npv: number;
    irr: number;
  };
}

const ProfitabilityMetrics: React.FC<ProfitabilityMetricsProps> = ({ metrics }) => {
  const getROIStatus = (roi: number) => {
    if (roi >= 25) return 'success';
    if (roi >= 15) return 'normal';
    return 'exception';
  };

  const getPaybackStatus = (years: number) => {
    if (years <= 2) return 'success';
    if (years <= 4) return 'normal';
    return 'exception';
  };

  return (
    <Card title="Profitability Analysis" className="h-full">
      <Row gutter={[16, 16]}>
        <Col xs={24} sm={12}>
          <Tooltip title="Annual revenue from operations">
            <Card className="metric-card">
              <Statistic
                title="Annual Revenue"
                value={metrics.annualRevenue}
                precision={2}
                prefix={<DollarOutlined />}
                formatter={value => formatCurrency(value as number)}
                valueStyle={{ color: '#3f8600' }}
              />
            </Card>
          </Tooltip>
        </Col>
        <Col xs={24} sm={12}>
          <Tooltip title="Annual profit (Revenue - Costs)">
            <Card className="metric-card">
              <Statistic
                title="Annual Profit"
                value={metrics.annualProfit}
                precision={2}
                prefix={<DollarOutlined />}
                formatter={value => formatCurrency(value as number)}
                valueStyle={{ color: metrics.annualProfit >= 0 ? '#3f8600' : '#cf1322' }}
              />
            </Card>
          </Tooltip>
        </Col>
        <Col xs={24} sm={12}>
          <Tooltip title="Return on Investment">
            <Card className="metric-card">
              <Statistic
                title="ROI"
                value={metrics.roi}
                precision={1}
                prefix={<PercentageOutlined />}
                suffix="%"
                valueStyle={{ color: metrics.roi >= 15 ? '#3f8600' : '#cf1322' }}
              />
              <Progress
                percent={Math.min(100, metrics.roi)}
                status={getROIStatus(metrics.roi)}
              />
            </Card>
          </Tooltip>
        </Col>
        <Col xs={24} sm={12}>
          <Tooltip title="Time required to recover the investment">
            <Card className="metric-card">
              <Statistic
                title="Payback Period"
                value={metrics.paybackPeriod}
                precision={1}
                prefix={<FieldTimeOutlined />}
                suffix="years"
                valueStyle={{ color: metrics.paybackPeriod <= 4 ? '#3f8600' : '#cf1322' }}
              />
              <Progress
                percent={Math.min(100, (5 / metrics.paybackPeriod) * 100)}
                status={getPaybackStatus(metrics.paybackPeriod)}
              />
            </Card>
          </Tooltip>
        </Col>
      </Row>
    </Card>
  );
};

export default ProfitabilityMetrics; 
"use client";

import React from 'react';
import { Card, Statistic, Row, Col, Progress, Tooltip } from 'antd';
import { 
  DollarOutlined, 
  PercentageOutlined,
  FieldTimeOutlined,
  RiseOutlined 
} from '@ant-design/icons';
import { formatCurrency } from '@/lib/formatters';

interface ProfitabilityMetricsProps {
  metrics: {
    npv: number;
    roi: number;
    paybackPeriod: number;
    irr: number;
  };
  totalInvestment: number;
  annualCosts: number;
}

const ProfitabilityMetrics: React.FC<ProfitabilityMetricsProps> = ({ 
  metrics,
  totalInvestment,
  annualCosts
}) => {
  const getMetricStatus = (value: number, thresholds: { low: number; medium: number }) => {
    if (value >= thresholds.medium) return { color: '#3f8600', status: 'success' as const };
    if (value >= thresholds.low) return { color: '#faad14', status: 'normal' as const };
    return { color: '#cf1322', status: 'exception' as const };
  };

  const metrics_config = [
    {
      title: 'Net Present Value',
      value: metrics.npv,
      prefix: <DollarOutlined />,
      formatter: (value: number) => formatCurrency(value),
      tooltip: 'Present value of future cash flows minus initial investment',
      thresholds: { low: 0, medium: totalInvestment * 0.2 }
    },
    {
      title: 'Return on Investment',
      value: metrics.roi,
      prefix: <PercentageOutlined />,
      suffix: '%',
      tooltip: 'Percentage return on initial investment',
      thresholds: { low: 15, medium: 25 }
    },
    {
      title: 'Internal Rate of Return',
      value: metrics.irr,
      prefix: <RiseOutlined />,
      suffix: '%',
      tooltip: 'Discount rate that makes NPV zero',
      thresholds: { low: 10, medium: 20 }
    },
    {
      title: 'Payback Period',
      value: metrics.paybackPeriod,
      prefix: <FieldTimeOutlined />,
      suffix: 'years',
      tooltip: 'Time required to recover the investment',
      thresholds: { low: 5, medium: 3 },
      inverse: true
    }
  ];

  return (
    <Card title="Profitability Analysis" className="h-full">
      <Row gutter={[16, 16]}>
        {metrics_config.map((metric, index) => {
          const status = getMetricStatus(
            metric.value,
            metric.inverse ? 
              { low: metric.thresholds.medium, medium: metric.thresholds.low } :
              metric.thresholds
          );

          return (
            <Col xs={24} sm={12} key={index}>
              <Tooltip title={metric.tooltip}>
                <Card className="metric-card">
                  <Statistic
                    title={metric.title}
                    value={metric.value}
                    precision={2}
                    prefix={metric.prefix}
                    suffix={metric.suffix}
                    valueStyle={{ color: status.color }}
                  />
                  <Progress
                    percent={
                      metric.inverse ?
                        Math.max(0, 100 - (metric.value / metric.thresholds.low) * 100) :
                        Math.min(100, (metric.value / metric.thresholds.medium) * 100)
                    }
                    status={status.status}
                    strokeColor={status.color}
                    size="small"
                    className="mt-2"
                  />
                </Card>
              </Tooltip>
            </Col>
          );
        })}
      </Row>
    </Card>
  );
};

export default ProfitabilityMetrics; 
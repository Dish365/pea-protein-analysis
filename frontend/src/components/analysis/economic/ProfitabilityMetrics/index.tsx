"use client";

import React from 'react';
import { Card, Statistic, Row, Col, Progress, Tooltip } from 'antd';
import { 
  DollarOutlined, 
  FieldTimeOutlined, 
  RiseOutlined,
  PercentageOutlined 
} from '@ant-design/icons';

interface ProfitabilityMetricsProps {
  totalCost: number;
  productionVolume: number;
  projectDuration: number;
  discountRate: number;
  equipmentCost: number;
  installationFactor: number;
}

export const ProfitabilityMetrics: React.FC<ProfitabilityMetricsProps> = ({
  totalCost,
  productionVolume,
  projectDuration,
  discountRate,
  equipmentCost,
  installationFactor,
}) => {
  // Calculate profitability metrics
  const totalInvestment = equipmentCost * (1 + installationFactor);
  const annualRevenue = calculateAnnualRevenue(productionVolume);
  const annualProfit = annualRevenue - totalCost;
  const roi = (annualProfit / totalInvestment) * 100;
  const paybackPeriod = totalInvestment / annualProfit;
  const npv = calculateNPV(annualProfit, discountRate, projectDuration, totalInvestment);
  const irr = calculateIRR(annualProfit, totalInvestment, projectDuration);

  return (
    <Card title="Profitability Analysis" className="profitability-metrics-card">
      <Row gutter={[16, 16]}>
        <Col xs={24} sm={12}>
          <Tooltip title="Annual revenue based on production volume">
            <Card className="metric-card">
              <Statistic
                title="Annual Revenue"
                value={annualRevenue}
                precision={2}
                prefix={<DollarOutlined />}
                suffix="USD"
                valueStyle={{ color: '#3f8600' }}
              />
            </Card>
          </Tooltip>
        </Col>
        <Col xs={24} sm={12}>
          <Tooltip title="Annual profit (Revenue - Total Cost)">
            <Card className="metric-card">
              <Statistic
                title="Annual Profit"
                value={annualProfit}
                precision={2}
                prefix={<DollarOutlined />}
                suffix="USD"
                valueStyle={{ color: annualProfit >= 0 ? '#3f8600' : '#cf1322' }}
              />
            </Card>
          </Tooltip>
        </Col>
      </Row>

      <Row gutter={[16, 16]} style={{ marginTop: '16px' }}>
        <Col xs={24} sm={12}>
          <Tooltip title="Return on Investment">
            <Card className="metric-card">
              <Statistic
                title="ROI"
                value={roi}
                precision={1}
                prefix={<RiseOutlined />}
                suffix="%"
                valueStyle={{ color: roi >= 15 ? '#3f8600' : '#cf1322' }}
              />
              <Progress
                percent={Math.min(100, roi)}
                status={roi >= 15 ? 'success' : 'normal'}
                strokeColor={roi >= 15 ? '#52c41a' : '#1890ff'}
              />
            </Card>
          </Tooltip>
        </Col>
        <Col xs={24} sm={12}>
          <Tooltip title="Time required to recover the investment">
            <Card className="metric-card">
              <Statistic
                title="Payback Period"
                value={paybackPeriod}
                precision={1}
                prefix={<FieldTimeOutlined />}
                suffix="years"
                valueStyle={{ color: paybackPeriod <= 5 ? '#3f8600' : '#cf1322' }}
              />
              <Progress
                percent={Math.min(100, (5 / paybackPeriod) * 100)}
                status={paybackPeriod <= 5 ? 'success' : 'normal'}
                strokeColor={paybackPeriod <= 5 ? '#52c41a' : '#1890ff'}
              />
            </Card>
          </Tooltip>
        </Col>
      </Row>

      <Row gutter={[16, 16]} style={{ marginTop: '16px' }}>
        <Col xs={24} sm={12}>
          <Tooltip title="Net Present Value">
            <Card className="metric-card">
              <Statistic
                title="NPV"
                value={npv}
                precision={2}
                prefix={<DollarOutlined />}
                suffix="USD"
                valueStyle={{ color: npv >= 0 ? '#3f8600' : '#cf1322' }}
              />
            </Card>
          </Tooltip>
        </Col>
        <Col xs={24} sm={12}>
          <Tooltip title="Internal Rate of Return">
            <Card className="metric-card">
              <Statistic
                title="IRR"
                value={irr}
                precision={1}
                prefix={<PercentageOutlined />}
                suffix="%"
                valueStyle={{ color: irr >= discountRate ? '#3f8600' : '#cf1322' }}
              />
            </Card>
          </Tooltip>
        </Col>
      </Row>
    </Card>
  );
};

// Helper functions for financial calculations
function calculateAnnualRevenue(productionVolume: number): number {
  const averageSellingPrice = 5.0; // USD/kg - This should be configurable
  return productionVolume * averageSellingPrice;
}

function calculateNPV(
  annualCashFlow: number,
  discountRate: number,
  years: number,
  initialInvestment: number
): number {
  let npv = -initialInvestment;
  for (let t = 1; t <= years; t++) {
    npv += annualCashFlow / Math.pow(1 + discountRate, t);
  }
  return npv;
}

function calculateIRR(
  annualCashFlow: number,
  initialInvestment: number,
  years: number
): number {
  // Simple IRR approximation
  const averageAnnualReturn = (annualCashFlow * years - initialInvestment) / initialInvestment;
  return (averageAnnualReturn / years) * 100;
}

export default ProfitabilityMetrics;

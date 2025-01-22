"use client";

import React from 'react';
import { Card, Statistic, Row, Col, Progress, Tooltip } from 'antd';
import { ExperimentOutlined, PercentageOutlined } from '@ant-design/icons';

interface ProteinRecoveryCardProps {
  initialProtein: number;
  finalProtein: number;
  inputMass: number;
  outputMass: number;
}

const ProteinRecoveryCard: React.FC<ProteinRecoveryCardProps> = ({
  initialProtein,
  finalProtein,
  inputMass,
  outputMass,
}) => {
  // Calculate protein recovery metrics
  const initialProteinMass = (initialProtein / 100) * inputMass;
  const finalProteinMass = (finalProtein / 100) * outputMass;
  const proteinRecoveryRate = (finalProteinMass / initialProteinMass) * 100;
  const proteinConcentrationIncrease = ((finalProtein - initialProtein) / initialProtein) * 100;

  return (
    <Card title="Protein Recovery Analysis" className="protein-recovery-card">
      <Row gutter={[16, 16]}>
        <Col xs={24} sm={12}>
          <Tooltip title="Total protein mass before processing">
            <Statistic
              title="Initial Protein Mass"
              value={initialProteinMass.toFixed(2)}
              suffix="kg"
              prefix={<ExperimentOutlined />}
            />
          </Tooltip>
        </Col>
        <Col xs={24} sm={12}>
          <Tooltip title="Total protein mass after processing">
            <Statistic
              title="Final Protein Mass"
              value={finalProteinMass.toFixed(2)}
              suffix="kg"
              prefix={<ExperimentOutlined />}
            />
          </Tooltip>
        </Col>
      </Row>

      <div className="recovery-metrics" style={{ marginTop: '24px' }}>
        <Row gutter={[16, 16]}>
          <Col xs={24} sm={12}>
            <Tooltip title="Percentage of initial protein recovered in final product">
              <Card className="metric-card">
                <Statistic
                  title="Protein Recovery Rate"
                  value={proteinRecoveryRate}
                  precision={1}
                  suffix="%"
                  prefix={<ExperimentOutlined />}
                />
                <Progress
                  percent={proteinRecoveryRate}
                  status={proteinRecoveryRate >= 90 ? 'success' : 'normal'}
                  strokeColor={proteinRecoveryRate >= 90 ? '#52c41a' : '#1890ff'}
                />
              </Card>
            </Tooltip>
          </Col>
          <Col xs={24} sm={12}>
            <Tooltip title="Percentage increase in protein concentration">
              <Card className="metric-card">
                <Statistic
                  title="Concentration Increase"
                  value={proteinConcentrationIncrease}
                  precision={1}
                  suffix="%"
                  prefix={<PercentageOutlined />}
                  valueStyle={{ color: proteinConcentrationIncrease > 0 ? '#3f8600' : '#cf1322' }}
                />
                <Progress
                  percent={Math.min(100, Math.max(0, proteinConcentrationIncrease))}
                  status={proteinConcentrationIncrease > 10 ? 'success' : 'normal'}
                  strokeColor={proteinConcentrationIncrease > 10 ? '#52c41a' : '#1890ff'}
                />
              </Card>
            </Tooltip>
          </Col>
        </Row>
      </div>
    </Card>
  );
};

export default ProteinRecoveryCard;

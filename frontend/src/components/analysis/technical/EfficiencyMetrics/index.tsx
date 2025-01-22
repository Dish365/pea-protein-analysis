"use client";

import React from 'react';
import { Card, Statistic, Row, Col, Progress, Tooltip } from 'antd';
import { ProcessType } from '../../../../types/process';
import { 
  ThunderboltOutlined, 
  DeploymentUnitOutlined, 
  DashboardOutlined,
  AimOutlined 
} from '@ant-design/icons';

interface EfficiencyMetricsProps {
  processType: ProcessType;
  inputMass: number;
  outputMass: number;
  airFlow: number;
  classifierSpeed: number;
}

const EfficiencyMetrics: React.FC<EfficiencyMetricsProps> = ({
  processType,
  inputMass,
  outputMass,
  airFlow,
  classifierSpeed,
}) => {
  // Calculate efficiency metrics
  const massEfficiency = (outputMass / inputMass) * 100;
  const processEfficiency = calculateProcessEfficiency(processType, airFlow, classifierSpeed);
  const throughputRate = calculateThroughput(inputMass, airFlow);
  const classifierEfficiency = calculateClassifierEfficiency(classifierSpeed);

  return (
    <Card title="Process Efficiency Metrics" className="efficiency-metrics-card">
      <Row gutter={[16, 16]}>
        <Col xs={24} sm={12}>
          <Tooltip title="Ratio of output mass to input mass">
            <Card className="metric-card">
              <Statistic
                title="Mass Efficiency"
                value={massEfficiency}
                precision={1}
                suffix="%"
                prefix={<DeploymentUnitOutlined />}
              />
              <Progress
                percent={massEfficiency}
                status={massEfficiency >= 85 ? 'success' : 'normal'}
                strokeColor={massEfficiency >= 85 ? '#52c41a' : '#1890ff'}
              />
            </Card>
          </Tooltip>
        </Col>
        <Col xs={24} sm={12}>
          <Tooltip title="Overall process efficiency based on type and parameters">
            <Card className="metric-card">
              <Statistic
                title="Process Efficiency"
                value={processEfficiency}
                precision={1}
                suffix="%"
                prefix={<ThunderboltOutlined />}
              />
              <Progress
                percent={processEfficiency}
                status={processEfficiency >= 90 ? 'success' : 'normal'}
                strokeColor={processEfficiency >= 90 ? '#52c41a' : '#1890ff'}
              />
            </Card>
          </Tooltip>
        </Col>
        <Col xs={24} sm={12}>
          <Tooltip title="Material processing rate">
            <Card className="metric-card">
              <Statistic
                title="Throughput Rate"
                value={throughputRate}
                precision={2}
                suffix="kg/h"
                prefix={<DashboardOutlined />}
              />
              <Progress
                percent={(throughputRate / 100) * 100}
                status={throughputRate >= 80 ? 'success' : 'normal'}
                strokeColor={throughputRate >= 80 ? '#52c41a' : '#1890ff'}
              />
            </Card>
          </Tooltip>
        </Col>
        <Col xs={24} sm={12}>
          <Tooltip title="Classifier performance efficiency">
            <Card className="metric-card">
              <Statistic
                title="Classifier Efficiency"
                value={classifierEfficiency}
                precision={1}
                suffix="%"
                prefix={<AimOutlined />}
              />
              <Progress
                percent={classifierEfficiency}
                status={classifierEfficiency >= 95 ? 'success' : 'normal'}
                strokeColor={classifierEfficiency >= 95 ? '#52c41a' : '#1890ff'}
              />
            </Card>
          </Tooltip>
        </Col>
      </Row>
    </Card>
  );
};

// Helper functions for efficiency calculations
function calculateProcessEfficiency(type: ProcessType, airFlow: number, classifierSpeed: number): number {
  const baseEfficiency = 85; // Base efficiency percentage
  let efficiency = baseEfficiency;

  switch (type) {
    case ProcessType.RF:
      efficiency += 5; // RF process typically has higher efficiency
      break;
    case ProcessType.IR:
      efficiency += 3; // IR process has moderate efficiency boost
      break;
    default:
      break;
  }

  // Adjust for air flow (optimal range: 400-600 m³/h)
  if (airFlow >= 400 && airFlow <= 600) {
    efficiency += 5;
  } else {
    efficiency -= Math.min(5, Math.abs(airFlow - 500) / 100);
  }

  // Adjust for classifier speed (optimal range: 1200-1800 rpm)
  if (classifierSpeed >= 1200 && classifierSpeed <= 1800) {
    efficiency += 5;
  } else {
    efficiency -= Math.min(5, Math.abs(classifierSpeed - 1500) / 300);
  }

  return Math.min(100, Math.max(0, efficiency));
}

function calculateThroughput(inputMass: number, airFlow: number): number {
  // Simplified throughput calculation
  return (inputMass * airFlow) / 1000;
}

function calculateClassifierEfficiency(speed: number): number {
  // Optimal speed range: 1200-1800 rpm
  const optimalSpeed = 1500;
  const efficiency = 95 - Math.abs(speed - optimalSpeed) / 100;
  return Math.min(100, Math.max(0, efficiency));
}

export default EfficiencyMetrics;

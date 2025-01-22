"use client";

import React from 'react';
import { Card, Table, Tooltip, Tag, Row, Col, Statistic } from 'antd';
import { InfoCircleOutlined } from '@ant-design/icons';
import { ProcessType } from '../../../../types/process';

interface ResourceMetrics {
  electricity: { consumption: number; perKg: number };
  cooling: { consumption: number; perKg: number };
  water: { consumption: number; perKg: number };
  transport: { consumption: number; perKg: number };
}

interface ImpactMetricsProps {
  resourceMetrics: ResourceMetrics;
  equipmentMass: number;
  processType: ProcessType;
  allocationMethod: string;
  productionVolume: number;
}

export const ImpactMetrics: React.FC<ImpactMetricsProps> = ({
  resourceMetrics,
  equipmentMass,
  processType,
  allocationMethod,
  productionVolume,
}) => {
  // Calculate environmental impact metrics
  const impacts = calculateEnvironmentalImpacts(
    resourceMetrics,
    equipmentMass,
    processType,
    productionVolume
  );

  const columns = [
    {
      title: 'Impact Category',
      dataIndex: 'category',
      key: 'category',
      render: (text: string) => (
        <span>
          {text}
          <Tooltip title={getImpactDescription(text)}>
            <InfoCircleOutlined style={{ marginLeft: 8 }} />
          </Tooltip>
        </span>
      ),
    },
    {
      title: 'Total Impact',
      dataIndex: 'totalImpact',
      key: 'totalImpact',
      render: (value: number, record: any) => (
        <span>{formatImpactValue(value, record.unit)}</span>
      ),
    },
    {
      title: 'Per kg Product',
      dataIndex: 'perKg',
      key: 'perKg',
      render: (value: number, record: any) => (
        <span>{formatImpactValue(value, record.unit)}/kg</span>
      ),
    },
    {
      title: 'Status',
      dataIndex: 'status',
      key: 'status',
      render: (status: any) => (
        <Tag color={getStatusColor(status.performance)}>
          {status.performance}
        </Tag>
      ),
    },
  ];

  const data = [
    {
      key: '1',
      category: 'Global Warming Potential',
      totalImpact: impacts.gwp.total,
      perKg: impacts.gwp.perKg,
      unit: 'kg CO2 eq',
      status: { performance: getPerformanceLevel(impacts.gwp.perKg, 2.5) },
    },
    {
      key: '2',
      category: 'Energy Consumption',
      totalImpact: impacts.energy.total,
      perKg: impacts.energy.perKg,
      unit: 'MJ',
      status: { performance: getPerformanceLevel(impacts.energy.perKg, 25) },
    },
    {
      key: '3',
      category: 'Water Footprint',
      totalImpact: impacts.water.total,
      perKg: impacts.water.perKg,
      unit: 'm³',
      status: { performance: getPerformanceLevel(impacts.water.perKg, 0.1) },
    },
    {
      key: '4',
      category: 'Resource Depletion',
      totalImpact: impacts.resources.total,
      perKg: impacts.resources.perKg,
      unit: 'kg Sb eq',
      status: { performance: getPerformanceLevel(impacts.resources.perKg, 0.001) },
    },
  ];

  return (
    <Card 
      title="Environmental Impact Assessment" 
      className="impact-metrics-card"
      extra={
        <Tooltip title="Impact allocation method">
          <Tag color="blue">{allocationMethod}</Tag>
        </Tooltip>
      }
    >
      <Table 
        columns={columns}
        dataSource={data}
        pagination={false}
        className="impact-table"
      />

      <Row gutter={[16, 16]} style={{ marginTop: '24px' }}>
        <Col xs={24} sm={8}>
          <Card size="small">
            <Statistic
              title="Equipment Mass"
              value={equipmentMass}
              suffix="kg"
              precision={0}
            />
          </Card>
        </Col>
        <Col xs={24} sm={8}>
          <Card size="small">
            <Statistic
              title="Process Type"
              value={processType}
              valueStyle={{ fontSize: '14px' }}
            />
          </Card>
        </Col>
        <Col xs={24} sm={8}>
          <Card size="small">
            <Statistic
              title="Production Volume"
              value={productionVolume}
              suffix="kg/year"
              precision={0}
            />
          </Card>
        </Col>
      </Row>
    </Card>
  );
};

// Helper functions
function calculateEnvironmentalImpacts(
  metrics: ResourceMetrics,
  equipmentMass: number,
  processType: ProcessType,
  productionVolume: number
) {
  // GWP factors (kg CO2 eq per unit)
  const gwpFactors = {
    electricity: 0.5, // per kWh
    cooling: 0.3, // per kWh
    water: 0.001, // per kg
    transport: 0.07, // per MJ
    equipment: 2.5, // per kg equipment
  };

  // Energy factors (MJ per unit)
  const energyFactors = {
    electricity: 3.6, // per kWh
    cooling: 2.5, // per kWh
    transport: 1.0, // per MJ
    equipment: 25, // per kg equipment
  };

  // Calculate impacts
  const gwp = {
    total: (
      metrics.electricity.consumption * gwpFactors.electricity +
      metrics.cooling.consumption * gwpFactors.cooling +
      metrics.water.consumption * gwpFactors.water +
      metrics.transport.consumption * gwpFactors.transport +
      equipmentMass * gwpFactors.equipment / 10 // Assuming 10-year lifespan
    ),
    get perKg() { return this.total / productionVolume; }
  };

  const energy = {
    total: (
      metrics.electricity.consumption * energyFactors.electricity +
      metrics.cooling.consumption * energyFactors.cooling +
      metrics.transport.consumption * energyFactors.transport +
      equipmentMass * energyFactors.equipment / 10
    ),
    get perKg() { return this.total / productionVolume; }
  };

  const water = {
    total: metrics.water.consumption,
    get perKg() { return this.total / productionVolume; }
  };

  const resources = {
    total: equipmentMass * 0.001, // Simplified resource depletion calculation
    get perKg() { return this.total / productionVolume; }
  };

  return { gwp, energy, water, resources };
}

function getImpactDescription(category: string): string {
  const descriptions: Record<string, string> = {
    'Global Warming Potential': 'Carbon dioxide equivalent emissions from process operations',
    'Energy Consumption': 'Total energy consumption including electricity, cooling, and transport',
    'Water Footprint': 'Total water consumption in the process',
    'Resource Depletion': 'Impact on non-renewable resource depletion',
  };
  return descriptions[category] || category;
}

function formatImpactValue(value: number, unit: string): string {
  if (value < 0.01) {
    return `${(value * 1000).toFixed(2)} m${unit}`;
  }
  if (value > 1000) {
    return `${(value / 1000).toFixed(2)} k${unit}`;
  }
  return `${value.toFixed(2)} ${unit}`;
}

function getPerformanceLevel(value: number, threshold: number): string {
  if (value <= threshold * 0.8) return 'Excellent';
  if (value <= threshold) return 'Good';
  if (value <= threshold * 1.2) return 'Fair';
  return 'Poor';
}

function getStatusColor(performance: string): string {
  const colors: Record<string, string> = {
    'Excellent': 'green',
    'Good': 'blue',
    'Fair': 'orange',
    'Poor': 'red',
  };
  return colors[performance] || 'default';
}

export default ImpactMetrics;

"use client";

import React, { useMemo } from 'react';
import { Card, Table, Tooltip, Tag } from 'antd';
import { InfoCircleOutlined } from '@ant-design/icons';

interface BaseValues {
  equipmentCost: number;
  maintenanceCost: number;
  rawMaterialCost: number;
  utilityCost: number;
  laborCost: number;
  productionVolume: number;
}

interface SensitivityAnalysisProps {
  baseValues: BaseValues;
  sensitivityRange: number;
  steps: number;
}

export const SensitivityAnalysis: React.FC<SensitivityAnalysisProps> = ({
  baseValues,
  sensitivityRange,
  steps,
}) => {
  const sensitivityData = useMemo(() => {
    return calculateSensitivityData(baseValues, sensitivityRange, steps);
  }, [baseValues, sensitivityRange, steps]);

  const columns = [
    {
      title: 'Parameter',
      dataIndex: 'parameter',
      key: 'parameter',
      render: (text: string) => (
        <span>
          {text}
          <Tooltip title={getParameterDescription(text)}>
            <InfoCircleOutlined style={{ marginLeft: 8 }} />
          </Tooltip>
        </span>
      ),
    },
    {
      title: 'Base Value',
      dataIndex: 'baseValue',
      key: 'baseValue',
      render: (value: number) => formatValue(value),
    },
    {
      title: 'Impact on Profitability',
      dataIndex: 'impact',
      key: 'impact',
      render: (impact: number) => (
        <Tag color={getImpactColor(impact)}>
          {impact >= 0 ? '+' : ''}{impact.toFixed(1)}%
        </Tag>
      ),
    },
    {
      title: 'Sensitivity',
      dataIndex: 'sensitivity',
      key: 'sensitivity',
      render: (sensitivity: string) => (
        <Tag color={getSensitivityColor(sensitivity)}>
          {sensitivity}
        </Tag>
      ),
    },
  ];

  return (
    <Card 
      title="Sensitivity Analysis" 
      className="sensitivity-analysis-card"
      extra={
        <Tooltip title="Analysis of how changes in parameters affect profitability">
          <InfoCircleOutlined />
        </Tooltip>
      }
    >
      <Table 
        columns={columns}
        dataSource={sensitivityData}
        pagination={false}
        className="sensitivity-table"
      />
    </Card>
  );
};

// Helper functions
function calculateSensitivityData(
  baseValues: BaseValues,
  sensitivityRange: number,
  steps: number
) {
  const parameters = Object.entries(baseValues);
  return parameters.map(([key, value]) => {
    const impact = calculateParameterImpact(key as keyof BaseValues, value, baseValues);
    return {
      key,
      parameter: formatParameterName(key),
      baseValue: value,
      impact,
      sensitivity: categorizeSensitivity(impact),
    };
  });
}

function calculateParameterImpact(
  parameter: keyof BaseValues,
  value: number,
  baseValues: BaseValues
): number {
  // Simplified impact calculation
  const variation = value * 0.1; // 10% change
  const baseProfit = calculateProfit(baseValues);
  const modifiedValues = { ...baseValues, [parameter]: value + variation };
  const modifiedProfit = calculateProfit(modifiedValues);
  
  return ((modifiedProfit - baseProfit) / baseProfit) * 100;
}

function calculateProfit(values: BaseValues): number {
  const revenue = values.productionVolume * 5.0; // Assuming $5/kg selling price
  const costs = values.equipmentCost / 10 + // Assuming 10-year depreciation
                values.maintenanceCost +
                values.rawMaterialCost * values.productionVolume +
                values.utilityCost * values.productionVolume +
                values.laborCost * values.productionVolume;
  return revenue - costs;
}

function formatParameterName(key: string): string {
  return key
    .replace(/([A-Z])/g, ' $1')
    .replace(/^./, str => str.toUpperCase());
}

function getParameterDescription(parameter: string): string {
  const descriptions: Record<string, string> = {
    'Equipment Cost': 'Initial investment in processing equipment',
    'Maintenance Cost': 'Annual cost of equipment maintenance',
    'Raw Material Cost': 'Cost per kg of input material',
    'Utility Cost': 'Cost of utilities per kg of production',
    'Labor Cost': 'Labor cost per kg of production',
    'Production Volume': 'Annual production volume in kg',
  };
  return descriptions[parameter] || parameter;
}

function formatValue(value: number): string {
  if (value >= 1000000) {
    return `$${(value / 1000000).toFixed(2)}M`;
  } else if (value >= 1000) {
    return `$${(value / 1000).toFixed(2)}K`;
  }
  return `$${value.toFixed(2)}`;
}

function getImpactColor(impact: number): string {
  if (Math.abs(impact) < 5) return 'blue';
  if (impact >= 5) return 'green';
  return 'red';
}

function categorizeSensitivity(impact: number): string {
  const absImpact = Math.abs(impact);
  if (absImpact < 5) return 'Low';
  if (absImpact < 15) return 'Medium';
  return 'High';
}

function getSensitivityColor(sensitivity: string): string {
  const colors: Record<string, string> = {
    'Low': 'green',
    'Medium': 'gold',
    'High': 'red',
  };
  return colors[sensitivity] || 'default';
}

export default SensitivityAnalysis;

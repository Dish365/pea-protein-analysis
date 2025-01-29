"use client";

import React from 'react';
import { Card, Table, Tag, Tooltip, Typography } from 'antd';
import { InfoCircleOutlined } from '@ant-design/icons';
import { formatCurrency } from '@/lib/formatters';

const { Text } = Typography;

interface SensitivityParameter {
  parameter: string;
  baseValue: number;
  impact: number;
  sensitivity: 'Low' | 'Medium' | 'High';
  npvRange: [number, number];
  roiRange: [number, number];
}

interface SensitivityAnalysisProps {
  capex: {
    total_capex: number;
    equipment_cost: number;
  };
  opex: {
    total_opex: number;
  };
  profitability: {
    npv: number;
    roi: number;
    sensitivity_analysis?: {
      variables: string[];
      ranges: {
        [key: string]: {
          npv_impact: [number, number];
          roi_impact: [number, number];
          sensitivity: 'Low' | 'Medium' | 'High';
        };
      };
    };
  };
}

const SensitivityAnalysis: React.FC<SensitivityAnalysisProps> = ({
  capex,
  opex,
  profitability
}) => {
  // Transform backend data into table format
  const sensitivityData: SensitivityParameter[] = React.useMemo(() => {
    if (!profitability.sensitivity_analysis) return [];

    return Object.entries(profitability.sensitivity_analysis.ranges).map(([param, analysis]) => {
      // Calculate impact percentage on NPV
      const avgNpvImpact = ((analysis.npv_impact[1] - analysis.npv_impact[0]) / profitability.npv) * 100;

      return {
        parameter: param.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase()),
        baseValue: param === 'discount_rate' ? profitability.roi : 
                  param === 'production_volume' ? capex.total_capex : 
                  opex.total_opex,
        impact: Math.abs(avgNpvImpact),
        sensitivity: analysis.sensitivity,
        npvRange: analysis.npv_impact,
        roiRange: analysis.roi_impact
      };
    });
  }, [profitability, capex, opex]);

  const columns = [
    {
      title: 'Parameter',
      dataIndex: 'parameter',
      key: 'parameter',
      render: (text: string) => (
        <span className="flex items-center">
          {text}
          <Tooltip title={`Impact of changes in ${text.toLowerCase()} on profitability metrics`}>
            <InfoCircleOutlined className="ml-2 text-gray-400" />
          </Tooltip>
        </span>
      ),
    },
    {
      title: 'Base Value',
      dataIndex: 'baseValue',
      key: 'baseValue',
      render: (value: number, record: SensitivityParameter) => (
        <Text>
          {record.parameter.includes('Rate') ? 
            `${(value * 100).toFixed(1)}%` : 
            formatCurrency(value)
          }
        </Text>
      ),
    },
    {
      title: 'NPV Range',
      key: 'npvRange',
      render: (_: unknown, record: SensitivityParameter) => (
        <Tooltip title="Potential NPV range based on parameter variation">
          <span>
            {formatCurrency(record.npvRange[0])} to {formatCurrency(record.npvRange[1])}
          </span>
        </Tooltip>
      ),
    },
    {
      title: 'Impact on NPV',
      dataIndex: 'impact',
      key: 'impact',
      render: (impact: number) => (
        <Text className={impact > 20 ? 'text-red-500' : impact > 10 ? 'text-orange-500' : 'text-green-500'}>
          {impact >= 0 ? '+' : ''}{impact.toFixed(1)}%
        </Text>
      ),
    },
    {
      title: 'Sensitivity',
      dataIndex: 'sensitivity',
      key: 'sensitivity',
      render: (sensitivity: string) => {
        const color = 
          sensitivity === 'High' ? 'red' :
          sensitivity === 'Medium' ? 'orange' : 'green';
        return <Tag color={color}>{sensitivity}</Tag>;
      },
    },
  ];

  return (
    <Card 
      title="Sensitivity Analysis" 
      className="sensitivity-analysis-card"
      extra={
        <Tooltip title="Analysis of how changes in key parameters affect project profitability">
          <InfoCircleOutlined className="text-gray-400" />
        </Tooltip>
      }
    >
      <Table 
        columns={columns}
        dataSource={sensitivityData}
        pagination={false}
        rowKey="parameter"
        className="sensitivity-table"
        summary={() => (
          <Table.Summary>
            <Table.Summary.Row>
              <Table.Summary.Cell index={0} colSpan={5}>
                <Text type="secondary" className="text-sm">
                  * Sensitivity ranges are calculated using ±{(profitability.sensitivity_analysis?.ranges?.discount_rate?.sensitivity === 'High' ? 20 : 10)}% variation in parameters
                </Text>
              </Table.Summary.Cell>
            </Table.Summary.Row>
          </Table.Summary>
        )}
      />
    </Card>
  );
};

export default SensitivityAnalysis; 
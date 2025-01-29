"use client";

import React from 'react';
import { Row, Col, Card, Statistic, Table, Progress, Tooltip } from 'antd';
import { 
  DollarOutlined, 
  RiseOutlined, 
  ClockCircleOutlined,
  PercentageOutlined
} from '@ant-design/icons';
import { Area } from '@ant-design/plots';
import { EconomicAnalysisResult } from '@/types/economic';

interface EconomicAnalysisViewProps {
  data: EconomicAnalysisResult;
}

const EconomicAnalysisView: React.FC<EconomicAnalysisViewProps> = ({ data }) => {
  // Key financial metrics
  const keyMetrics = [
    {
      title: 'Net Present Value',
      value: data.profitability_analysis.npv,
      prefix: <DollarOutlined />,
      suffix: 'USD',
      precision: 0,
      color: data.profitability_analysis.npv > 0 ? '#52c41a' : '#f5222d'
    },
    {
      title: 'Return on Investment',
      value: data.profitability_analysis.roi,
      prefix: <PercentageOutlined />,
      suffix: '%',
      precision: 1,
      color: data.profitability_analysis.roi > 15 ? '#52c41a' : '#faad14'
    },
    {
      title: 'Payback Period',
      value: data.profitability_analysis.payback_period,
      prefix: <ClockCircleOutlined />,
      suffix: 'years',
      precision: 1,
      color: data.profitability_analysis.payback_period < 5 ? '#52c41a' : '#faad14'
    },
    {
      title: 'IRR',
      value: data.profitability_analysis.irr,
      prefix: <RiseOutlined />,
      suffix: '%',
      precision: 1,
      color: data.profitability_analysis.irr > 20 ? '#52c41a' : '#faad14'
    }
  ];

  // CAPEX breakdown data
  const capexData = [
    {
      key: 'equipment',
      category: 'Equipment Cost',
      amount: data.capex_analysis.equipment_cost,
      percentage: (data.capex_analysis.equipment_cost / data.capex_analysis.total_capex) * 100
    },
    {
      key: 'installation',
      category: 'Installation Cost',
      amount: data.capex_analysis.installation_cost,
      percentage: (data.capex_analysis.installation_cost / data.capex_analysis.total_capex) * 100
    },
    {
      key: 'indirect',
      category: 'Indirect Cost',
      amount: data.capex_analysis.indirect_cost,
      percentage: (data.capex_analysis.indirect_cost / data.capex_analysis.total_capex) * 100
    }
  ];

  // OPEX breakdown data
  const opexData = [
    {
      key: 'utilities',
      category: 'Utilities',
      amount: data.opex_analysis.utilities_cost,
      percentage: (data.opex_analysis.utilities_cost / data.opex_analysis.total_opex) * 100
    },
    {
      key: 'materials',
      category: 'Materials',
      amount: data.opex_analysis.materials_cost,
      percentage: (data.opex_analysis.materials_cost / data.opex_analysis.total_opex) * 100
    },
    {
      key: 'labor',
      category: 'Labor',
      amount: data.opex_analysis.labor_cost,
      percentage: (data.opex_analysis.labor_cost / data.opex_analysis.total_opex) * 100
    },
    {
      key: 'maintenance',
      category: 'Maintenance',
      amount: data.opex_analysis.maintenance_cost,
      percentage: (data.opex_analysis.maintenance_cost / data.opex_analysis.total_opex) * 100
    }
  ];

  const columns = [
    {
      title: 'Category',
      dataIndex: 'category',
      key: 'category',
    },
    {
      title: 'Amount (USD)',
      dataIndex: 'amount',
      key: 'amount',
      render: (value: number) => `$${value.toLocaleString(undefined, { maximumFractionDigits: 0 })}`,
    },
    {
      title: 'Percentage',
      dataIndex: 'percentage',
      key: 'percentage',
      render: (value: number) => (
        <Tooltip title={`${value.toFixed(1)}%`}>
          <Progress percent={value} size="small" showInfo={false} />
        </Tooltip>
      ),
    },
  ];

  return (
    <div className="economic-analysis">
      <Row gutter={[16, 16]}>
        {/* Key Financial Metrics */}
        {keyMetrics.map((metric, index) => (
          <Col xs={24} sm={12} lg={6} key={index}>
            <Card>
              <Statistic
                title={metric.title}
                value={metric.value}
                precision={metric.precision}
                prefix={metric.prefix}
                suffix={metric.suffix}
                valueStyle={{ color: metric.color }}
              />
            </Card>
          </Col>
        ))}

        {/* CAPEX Analysis */}
        <Col xs={24} lg={12}>
          <Card title="Capital Expenditure (CAPEX) Breakdown" className="h-full">
            <Statistic
              title="Total CAPEX"
              value={data.capex_analysis.total_capex}
              prefix="$"
              precision={0}
              className="mb-4"
            />
            <Table
              dataSource={capexData}
              columns={columns}
              pagination={false}
              size="small"
            />
          </Card>
        </Col>

        {/* OPEX Analysis */}
        <Col xs={24} lg={12}>
          <Card title="Operating Expenditure (OPEX) Breakdown" className="h-full">
            <Statistic
              title="Total Annual OPEX"
              value={data.opex_analysis.total_opex}
              prefix="$"
              precision={0}
              className="mb-4"
            />
            <Table
              dataSource={opexData}
              columns={columns}
              pagination={false}
              size="small"
            />
          </Card>
        </Col>
      </Row>
    </div>
  );
};

export default EconomicAnalysisView;
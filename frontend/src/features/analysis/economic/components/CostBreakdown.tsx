"use client";

import React from 'react';
import { Card, Statistic, Row, Col, Progress, Tooltip, Tabs } from 'antd';
import { DollarOutlined, BuildOutlined, ThunderboltOutlined } from '@ant-design/icons';
import { formatCurrency } from '@/lib/formatters';

interface CostBreakdownProps {
  capex: {
    total_capex: number;
    equipment_cost: number;
    installation_cost: number;
    indirect_cost: number;
  };
  opex: {
    total_opex: number;
    utilities_cost: number;
    materials_cost: number;
    labor_cost: number;
    maintenance_cost: number;
  };
  totalInvestment: number;
  annualCosts: number;
}

const CostBreakdown: React.FC<CostBreakdownProps> = ({
  capex,
  opex,
  totalInvestment,
  annualCosts,
}) => {
  const capexItems = [
    {
      title: 'Equipment',
      value: capex.equipment_cost,
      color: '#1890ff',
      tooltip: 'Base equipment cost',
    },
    {
      title: 'Installation',
      value: capex.installation_cost,
      color: '#52c41a',
      tooltip: 'Equipment installation cost',
    },
    {
      title: 'Indirect Costs',
      value: capex.indirect_cost,
      color: '#faad14',
      tooltip: 'Engineering, construction, and contingency costs',
    },
  ];

  const opexItems = [
    {
      title: 'Utilities',
      value: opex.utilities_cost,
      color: '#722ed1',
      tooltip: 'Annual utility costs (electricity, water, etc.)',
    },
    {
      title: 'Materials',
      value: opex.materials_cost,
      color: '#eb2f96',
      tooltip: 'Annual raw material costs',
    },
    {
      title: 'Labor',
      value: opex.labor_cost,
      color: '#f5222d',
      tooltip: 'Annual labor costs',
    },
    {
      title: 'Maintenance',
      value: opex.maintenance_cost,
      color: '#fa541c',
      tooltip: 'Annual maintenance costs',
    },
  ];

  return (
    <Card title="Cost Analysis" className="h-full">
      <Tabs
        items={[
          {
            key: 'capex',
            label: (
              <span>
                <BuildOutlined /> Capital Expenditure
              </span>
            ),
            children: (
              <>
                <Statistic
                  title="Total Investment"
                  value={totalInvestment}
                  prefix={<DollarOutlined />}
                  formatter={value => formatCurrency(value as number)}
                  className="mb-4"
                />
                <div className="cost-breakdown">
                  {capexItems.map((item, index) => (
                    <Tooltip key={index} title={item.tooltip}>
                      <div className="mb-4">
                        <div className="flex justify-between mb-1">
                          <span>{item.title}</span>
                          <span>
                            {formatCurrency(item.value)} (
                            {((item.value / totalInvestment) * 100).toFixed(1)}%)
                          </span>
                        </div>
                        <Progress
                          percent={(item.value / totalInvestment) * 100}
                          strokeColor={item.color}
                          showInfo={false}
                        />
                      </div>
                    </Tooltip>
                  ))}
                </div>
              </>
            ),
          },
          {
            key: 'opex',
            label: (
              <span>
                <ThunderboltOutlined /> Operating Expenses
              </span>
            ),
            children: (
              <>
                <Statistic
                  title="Annual Operating Costs"
                  value={annualCosts}
                  prefix={<DollarOutlined />}
                  formatter={value => formatCurrency(value as number)}
                  className="mb-4"
                />
                <div className="cost-breakdown">
                  {opexItems.map((item, index) => (
                    <Tooltip key={index} title={item.tooltip}>
                      <div className="mb-4">
                        <div className="flex justify-between mb-1">
                          <span>{item.title}</span>
                          <span>
                            {formatCurrency(item.value)} (
                            {((item.value / annualCosts) * 100).toFixed(1)}%)
                          </span>
                        </div>
                        <Progress
                          percent={(item.value / annualCosts) * 100}
                          strokeColor={item.color}
                          showInfo={false}
                        />
                      </div>
                    </Tooltip>
                  ))}
                </div>
              </>
            ),
          },
        ]}
      />
    </Card>
  );
};

export default CostBreakdown; 
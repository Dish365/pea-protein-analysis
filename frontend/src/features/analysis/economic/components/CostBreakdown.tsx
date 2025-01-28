"use client";

import React from 'react';
import { Card, Statistic, Row, Col, Progress, Tooltip } from 'antd';
import { DollarOutlined } from '@ant-design/icons';
import { formatCurrency } from '@/lib/formatters';

interface CostBreakdownProps {
  costs: {
    equipment: number;
    maintenance: number;
    rawMaterial: number;
    utilities: number;
    labor: number;
    indirect: number;
  };
  totalCost: number;
  unitCost: number;
}

const CostBreakdown: React.FC<CostBreakdownProps> = ({
  costs,
  totalCost,
  unitCost,
}) => {
  const costItems = [
    {
      title: 'Equipment',
      value: costs.equipment,
      color: '#1890ff',
      tooltip: 'Annual equipment cost including installation',
    },
    {
      title: 'Maintenance',
      value: costs.maintenance,
      color: '#52c41a',
      tooltip: 'Annual maintenance cost',
    },
    {
      title: 'Raw Material',
      value: costs.rawMaterial,
      color: '#faad14',
      tooltip: 'Annual raw material cost',
    },
    {
      title: 'Utilities',
      value: costs.utilities,
      color: '#722ed1',
      tooltip: 'Annual utility costs',
    },
    {
      title: 'Labor',
      value: costs.labor,
      color: '#eb2f96',
      tooltip: 'Annual labor costs',
    },
    {
      title: 'Indirect',
      value: costs.indirect,
      color: '#f5222d',
      tooltip: 'Annual indirect costs',
    },
  ];

  return (
    <Card title="Cost Analysis" className="h-full">
      <Row gutter={[16, 16]} className="mb-6">
        <Col xs={24} sm={12}>
          <Tooltip title="Total annual cost of operation">
            <Statistic
              title="Total Annual Cost"
              value={totalCost}
              precision={2}
              prefix={<DollarOutlined />}
              formatter={value => formatCurrency(value as number)}
            />
          </Tooltip>
        </Col>
        <Col xs={24} sm={12}>
          <Tooltip title="Cost per unit of production">
            <Statistic
              title="Unit Cost"
              value={unitCost}
              precision={2}
              prefix={<DollarOutlined />}
              formatter={value => formatCurrency(value as number)}
              suffix="/unit"
            />
          </Tooltip>
        </Col>
      </Row>

      <div className="cost-breakdown">
        {costItems.map((item, index) => (
          <Tooltip key={index} title={item.tooltip}>
            <div className="mb-4">
              <div className="flex justify-between mb-1">
                <span>{item.title}</span>
                <span>{formatCurrency(item.value)} ({((item.value / totalCost) * 100).toFixed(1)}%)</span>
              </div>
              <Progress
                percent={(item.value / totalCost) * 100}
                strokeColor={item.color}
                showInfo={false}
              />
            </div>
          </Tooltip>
        ))}
      </div>
    </Card>
  );
};

export default CostBreakdown; 
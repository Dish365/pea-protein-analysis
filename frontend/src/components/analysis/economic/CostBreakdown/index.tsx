"use client";

import React from 'react';
import { Card, Statistic, Row, Col, Progress, Tooltip } from 'antd';
import { DollarOutlined, BarChartOutlined } from '@ant-design/icons';

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
  productionVolume: number;
  unitCost: number;
}

export const CostBreakdown: React.FC<CostBreakdownProps> = ({
  costs,
  totalCost,
  productionVolume,
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
      tooltip: 'Annual raw material cost based on production volume',
    },
    { 
      title: 'Utilities',
      value: costs.utilities,
      color: '#722ed1',
      tooltip: 'Annual utility costs based on production volume',
    },
    { 
      title: 'Labor',
      value: costs.labor,
      color: '#eb2f96',
      tooltip: 'Annual labor costs based on production volume',
    },
    { 
      title: 'Indirect',
      value: costs.indirect,
      color: '#f5222d',
      tooltip: 'Annual indirect costs based on equipment value',
    },
  ];

  return (
    <Card title="Cost Analysis" className="cost-breakdown-card">
      <Row gutter={[16, 16]}>
        <Col xs={24} sm={12}>
          <Tooltip title="Total annual cost of operation">
            <Statistic
              title="Total Annual Cost"
              value={totalCost}
              precision={2}
              prefix={<DollarOutlined />}
              suffix="USD"
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
              suffix="USD/kg"
            />
          </Tooltip>
        </Col>
      </Row>

      <div className="cost-breakdown" style={{ marginTop: '24px' }}>
        {costItems.map((item, index) => (
          <Tooltip key={index} title={item.tooltip}>
            <div className="cost-item" style={{ marginBottom: '16px' }}>
              <div className="cost-header" style={{ marginBottom: '8px' }}>
                <span>{item.title}</span>
                <span>
                  <DollarOutlined /> {item.value.toFixed(2)} ({((item.value / totalCost) * 100).toFixed(1)}%)
                </span>
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

      <div className="production-info" style={{ marginTop: '24px' }}>
        <Tooltip title="Annual production volume">
          <Card className="metric-card">
            <Statistic
              title="Production Volume"
              value={productionVolume}
              precision={0}
              prefix={<BarChartOutlined />}
              suffix="kg/year"
            />
          </Card>
        </Tooltip>
      </div>
    </Card>
  );
};

export default CostBreakdown;

"use client";

import React from 'react';
import { Layout, Row, Col, Statistic, Card as AntCard } from 'antd';
import { 
  ExperimentOutlined, 
  DollarOutlined, 
  EnvironmentOutlined 
} from '@ant-design/icons';
import Card from '../shared/Card';

const { Content } = Layout;

interface DashboardCardProps {
  title: string;
  icon: React.ReactNode;
  description: string;
  completed: number;
  inProgress: number;
  color: string;
  onClick?: () => void;
}

const DashboardCard: React.FC<DashboardCardProps> = ({
  title,
  icon,
  description,
  completed,
  inProgress,
  color,
  onClick
}) => (
  <Card 
    elevated
    hoverable
    onClick={onClick}
    className="h-full"
  >
    <div className="flex items-start gap-4">
      <div 
        className="p-3 rounded-lg"
        style={{ backgroundColor: `${color}15` }}
      >
        {React.cloneElement(icon as React.ReactElement, { 
          style: { fontSize: 24, color } 
        })}
      </div>
      <div className="flex-1">
        <h3 className="text-lg font-semibold mb-2">{title}</h3>
        <p className="text-gray-600 mb-4">{description}</p>
        <Row gutter={16}>
          <Col span={12}>
            <Statistic 
              title="Completed"
              value={completed}
              valueStyle={{ color: '#52c41a' }}
            />
          </Col>
          <Col span={12}>
            <Statistic 
              title="In Progress"
              value={inProgress}
              valueStyle={{ color: '#faad14' }}
            />
          </Col>
        </Row>
      </div>
    </div>
  </Card>
);

interface DashboardLayoutProps {
  children: React.ReactNode;
}

const DashboardLayout: React.FC<DashboardLayoutProps> = ({ children }) => {
  return (
    <Content className="p-6">
      <div className="max-w-7xl mx-auto">
        <Row gutter={[24, 24]}>
          <Col xs={24} lg={8}>
            <DashboardCard
              title="Technical Analysis"
              icon={<ExperimentOutlined />}
              description="Analyze process efficiency and performance metrics"
              completed={24}
              inProgress={3}
              color="#1890ff"
            />
          </Col>
          <Col xs={24} lg={8}>
            <DashboardCard
              title="Economic Analysis"
              icon={<DollarOutlined />}
              description="Evaluate costs, revenue, and profitability"
              completed={18}
              inProgress={2}
              color="#52c41a"
            />
          </Col>
          <Col xs={24} lg={8}>
            <DashboardCard
              title="Environmental Analysis"
              icon={<EnvironmentOutlined />}
              description="Assess environmental impact and sustainability"
              completed={15}
              inProgress={4}
              color="#722ed1"
            />
          </Col>
        </Row>
        <div className="mt-6">
          {children}
        </div>
      </div>
    </Content>
  );
};

export default DashboardLayout; 
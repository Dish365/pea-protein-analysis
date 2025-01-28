"use client";

import React from 'react';
import { Row, Col } from 'antd';
import { useRouter } from 'next/navigation';
import { 
  ExperimentOutlined, 
  DollarOutlined, 
  EnvironmentOutlined 
} from '@ant-design/icons';
import AnalysisCard from '@/components/ui/AnalysisCard';
import RecentAnalyses from '@/components/dashboard/RecentAnalyses';

export default function DashboardPage() {
  const router = useRouter();

  const analysisTypes = [
    {
      title: 'Technical Analysis',
      description: 'Analyze process efficiency and performance metrics',
      icon: <ExperimentOutlined style={{ fontSize: '24px' }} />,
      path: '/technical',
      color: '#1890ff',
      metrics: {
        completed: 24,
        inProgress: 3,
        trend: 12.5,
      },
    },
    {
      title: 'Economic Analysis',
      description: 'Evaluate costs, revenue, and profitability',
      icon: <DollarOutlined style={{ fontSize: '24px' }} />,
      path: '/economic',
      color: '#52c41a',
      metrics: {
        completed: 18,
        inProgress: 2,
      },
    },
    {
      title: 'Environmental Analysis',
      description: 'Assess environmental impact and sustainability',
      icon: <EnvironmentOutlined style={{ fontSize: '24px' }} />,
      path: '/environmental',
      color: '#722ed1',
      metrics: {
        completed: 15,
        inProgress: 4,
      },
    },
  ];

  return (
    <div className="p-6">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-2xl font-bold mb-6">Process Analysis Dashboard</h1>
        
        <Row gutter={[16, 16]}>
          {analysisTypes.map((analysis) => (
            <Col xs={24} md={8} key={analysis.path}>
              <AnalysisCard
                title={analysis.title}
                description={analysis.description}
                icon={analysis.icon}
                color={analysis.color}
                metrics={analysis.metrics}
                onClick={() => router.push(analysis.path)}
              />
            </Col>
          ))}
        </Row>

        <div className="mt-6">
          <RecentAnalyses />
        </div>
      </div>
    </div>
  );
} 
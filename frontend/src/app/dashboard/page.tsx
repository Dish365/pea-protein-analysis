"use client";

import React from 'react';
import { Card, Row, Col, Button, Typography } from 'antd';
import { ExperimentOutlined, DollarOutlined, EnvironmentOutlined } from '@ant-design/icons';
import { useRouter } from 'next/navigation';

const { Title, Paragraph } = Typography;

const Dashboard: React.FC = () => {
  const router = useRouter();

  const analysisTypes = [
    {
      title: 'Technical Analysis',
      description: 'Analyze process efficiency, protein recovery, and particle size distribution.',
      icon: <ExperimentOutlined style={{ fontSize: '24px' }} />,
      path: '/technical',
      color: '#1890ff',
    },
    {
      title: 'Economic Analysis',
      description: 'Evaluate costs, profitability metrics, and financial indicators.',
      icon: <DollarOutlined style={{ fontSize: '24px' }} />,
      path: '/economic',
      color: '#52c41a',
    },
    {
      title: 'Environmental Analysis',
      description: 'Assess environmental impact, resource usage, and sustainability metrics.',
      icon: <EnvironmentOutlined style={{ fontSize: '24px' }} />,
      path: '/environmental',
      color: '#722ed1',
    },
  ];

  return (
    <div className="dashboard" style={{ padding: '24px' }}>
      <Title level={2} style={{ marginBottom: '24px', textAlign: 'center' }}>
        Process Analysis Dashboard
      </Title>
      <Paragraph style={{ textAlign: 'center', marginBottom: '48px' }}>
        Select an analysis type to begin evaluating your process
      </Paragraph>

      <Row gutter={[24, 24]} justify="center">
        {analysisTypes.map((analysis) => (
          <Col xs={24} sm={12} md={8} key={analysis.title}>
            <Card
              hoverable
              style={{ height: '100%' }}
              bodyStyle={{ 
                display: 'flex', 
                flexDirection: 'column',
                height: '100%',
                alignItems: 'center',
                textAlign: 'center',
              }}
            >
              <div style={{ 
                color: analysis.color,
                marginBottom: '16px',
                padding: '16px',
                borderRadius: '50%',
                backgroundColor: `${analysis.color}15`,
              }}>
                {analysis.icon}
              </div>
              <Title level={3} style={{ marginTop: 0 }}>
                {analysis.title}
              </Title>
              <Paragraph style={{ flex: 1 }}>
                {analysis.description}
              </Paragraph>
              <Button
                type="primary"
                size="large"
                icon={analysis.icon}
                onClick={() => router.push(analysis.path)}
                style={{ 
                  backgroundColor: analysis.color,
                  borderColor: analysis.color,
                }}
              >
                Start Analysis
              </Button>
            </Card>
          </Col>
        ))}
      </Row>
    </div>
  );
};

export default Dashboard; 
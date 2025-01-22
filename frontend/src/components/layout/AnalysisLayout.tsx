"use client";

import React from 'react';
import { Layout, Menu } from 'antd';
import { ExperimentOutlined, DollarOutlined, EnvironmentOutlined, HomeOutlined } from '@ant-design/icons';
import { useRouter, usePathname } from 'next/navigation';

const { Header, Content } = Layout;

interface AnalysisLayoutProps {
  children: React.ReactNode;
}

const AnalysisLayout: React.FC<AnalysisLayoutProps> = ({ children }) => {
  const router = useRouter();
  const pathname = usePathname();

  const menuItems = [
    {
      key: '/',
      icon: <HomeOutlined />,
      label: 'Dashboard',
    },
    {
      key: '/technical',
      icon: <ExperimentOutlined />,
      label: 'Technical Analysis',
    },
    {
      key: '/economic',
      icon: <DollarOutlined />,
      label: 'Economic Analysis',
    },
    {
      key: '/environmental',
      icon: <EnvironmentOutlined />,
      label: 'Environmental Analysis',
    },
  ];

  return (
    <Layout style={{ minHeight: '100vh' }}>
      <Header style={{ padding: 0, background: '#fff', borderBottom: '1px solid #f0f0f0' }}>
        <Menu
          mode="horizontal"
          selectedKeys={[pathname || '/']}
          items={menuItems}
          onClick={({ key }) => router.push(key)}
          style={{ justifyContent: 'center' }}
        />
      </Header>
      <Content style={{ padding: '24px', background: '#f5f5f5' }}>
        <div style={{ background: '#fff', padding: '24px', borderRadius: '8px' }}>
          {children}
        </div>
      </Content>
    </Layout>
  );
};

export default AnalysisLayout; 
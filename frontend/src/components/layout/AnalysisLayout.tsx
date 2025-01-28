"use client";

import React from 'react';
import { Layout, Menu, Typography, Breadcrumb } from 'antd';
import { 
  ExperimentOutlined, 
  DollarOutlined, 
  EnvironmentOutlined, 
  DashboardOutlined 
} from '@ant-design/icons';
import { useRouter, usePathname } from 'next/navigation';
import Link from 'next/link';
import Card from '../shared/Card';

const { Header, Content } = Layout;
const { Title } = Typography;

interface AnalysisLayoutProps {
  children: React.ReactNode;
  title?: string;
  loading?: boolean;
}

const AnalysisLayout: React.FC<AnalysisLayoutProps> = ({ 
  children, 
  title,
  loading = false 
}) => {
  const router = useRouter();
  const pathname = usePathname();

  const menuItems = [
    {
      key: '/dashboard',
      icon: <DashboardOutlined />,
      label: 'Dashboard',
      color: '#1890ff'
    },
    {
      key: '/technical',
      icon: <ExperimentOutlined />,
      label: 'Technical Analysis',
      color: '#52c41a'
    },
    {
      key: '/economic',
      icon: <DollarOutlined />,
      label: 'Economic Analysis',
      color: '#faad14'
    },
    {
      key: '/environmental',
      icon: <EnvironmentOutlined />,
      label: 'Environmental Analysis',
      color: '#722ed1'
    },
  ];

  const getCurrentBreadcrumb = () => {
    const currentItem = menuItems.find(item => pathname?.includes(item.key));
    return currentItem?.label || 'Dashboard';
  };

  return (
    <Layout className="min-h-screen bg-gray-50">
      <Header className="bg-white px-6 shadow-sm fixed w-full z-10">
        <div className="max-w-7xl mx-auto flex items-center justify-between h-full">
          <Link href="/dashboard" className="text-xl font-bold text-gray-800 hover:text-primary">
            Process Analysis
          </Link>
          <Menu
            mode="horizontal"
            selectedKeys={[pathname || '/dashboard']}
            items={menuItems.map(item => ({
              ...item,
              className: pathname?.includes(item.key) ? `text-[${item.color}]` : ''
            }))}
            onClick={({ key }) => router.push(key)}
            className="border-none flex-1 justify-end"
          />
        </div>
      </Header>

      <Content className="mt-16 p-6">
        <div className="max-w-7xl mx-auto">
          <div className="mb-6">
            <Breadcrumb items={[
              { title: 'Home' },
              { title: getCurrentBreadcrumb() }
            ]} />
            {title && (
              <Title level={2} className="mt-4 mb-6">
                {title}
              </Title>
            )}
          </div>

          <Card 
            className="min-h-[calc(100vh-240px)]"
            elevated={false}
          >
            {children}
          </Card>
        </div>
      </Content>
    </Layout>
  );
};

export default AnalysisLayout; 
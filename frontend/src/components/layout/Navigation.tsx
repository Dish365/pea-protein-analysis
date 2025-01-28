"use client";

import React from 'react';
import { Layout, Menu } from 'antd';
import { usePathname, useRouter } from 'next/navigation';
import { 
  HomeOutlined, 
  ExperimentOutlined, 
  DollarOutlined, 
  EnvironmentOutlined 
} from '@ant-design/icons';

const { Header } = Layout;

const Navigation = () => {
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
    <Header className="bg-white border-b border-gray-200 px-6">
      <div className="max-w-7xl mx-auto flex items-center justify-between h-full">
        <div className="text-xl font-bold text-primary-600">
          Process Analysis
        </div>
        <Menu
          mode="horizontal"
          selectedKeys={[pathname || '/']}
          items={menuItems}
          onClick={({ key }) => router.push(key)}
          className="border-none flex-1 justify-end"
        />
      </div>
    </Header>
  );
};

export default Navigation; 
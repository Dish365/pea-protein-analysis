"use client";

import React, { useState } from "react";
import { Layout, Menu, message } from "antd";
import type { MenuProps } from 'antd';
import {
  DashboardOutlined,
  ExperimentOutlined,
  DollarOutlined,
  EnvironmentOutlined,
  UserOutlined,
  SettingOutlined,
  LogoutOutlined,
  MenuFoldOutlined,
  MenuUnfoldOutlined,
} from "@ant-design/icons";
import { useRouter, usePathname } from "next/navigation";
import { useAuth } from "@/hooks/useAuth";

const { Sider } = Layout;

type MenuItem = Required<MenuProps>['items'][number];

export default function SideNav() {
  const router = useRouter();
  const pathname = usePathname();
  const { signOut } = useAuth();
  const [collapsed, setCollapsed] = useState(false);

  const handleLogout = async () => {
    try {
      await signOut();
      message.success("Successfully logged out");
      router.push("/signin");
    } catch (error) {
      message.error("Failed to logout");
    }
  };

  const menuItems: MenuItem[] = [
    {
      key: "/dashboard",
      icon: <DashboardOutlined />,
      label: "Dashboard",
    },
    {
      key: "/dashboard/analysis/technical",
      icon: <ExperimentOutlined />,
      label: "Technical Analysis",
    },
    {
      key: "/dashboard/analysis/economic",
      icon: <DollarOutlined />,
      label: "Economic Analysis",
    },
    {
      key: "/dashboard/analysis/environmental",
      icon: <EnvironmentOutlined />,
      label: "Environmental Analysis",
    },
    {
      type: 'divider',
    },
    {
      key: "/dashboard/profile",
      icon: <UserOutlined />,
      label: "Profile",
    },
    {
      key: "/dashboard/settings",
      icon: <SettingOutlined />,
      label: "Settings",
    },
    {
      key: "logout",
      icon: <LogoutOutlined />,
      label: "Logout",
      danger: true,
    },
  ];

  return (
    <Sider
      width={250}
      collapsible
      collapsed={collapsed}
      onCollapse={(value) => setCollapsed(value)}
      trigger={null}
      className="fixed left-0"
      style={{
        height: 'calc(100vh - 64px)',
        marginTop: '64px',
        backgroundColor: '#fff',
      }}
    >
      <div className="flex justify-end p-4">
        <button
          onClick={() => setCollapsed(!collapsed)}
          className="text-gray-500 hover:text-gray-700 transition-colors"
        >
          {collapsed ? <MenuUnfoldOutlined /> : <MenuFoldOutlined />}
        </button>
      </div>
      <div className="h-[calc(100%-56px)] overflow-y-auto overflow-x-hidden">
        <Menu
          mode="inline"
          selectedKeys={[pathname || ""]}
          items={menuItems}
          onClick={({ key }) => {
            if (key === 'logout') {
              handleLogout();
            } else {
              router.push(key);
            }
          }}
          className="border-r"
          inlineCollapsed={collapsed}
        />
      </div>
    </Sider>
  );
} 
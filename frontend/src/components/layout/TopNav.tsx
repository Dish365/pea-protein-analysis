"use client";

import React from "react";
import { Layout, Menu, Button, Avatar, Dropdown, message } from "antd";
import { UserOutlined, SettingOutlined, LogoutOutlined } from "@ant-design/icons";
import { useRouter } from "next/navigation";
import { useUser } from "@/hooks/useUser";
import { useAuth } from "@/hooks/useAuth";

const { Header } = Layout;

export default function TopNav() {
  const router = useRouter();
  const { user } = useUser();
  const { signOut } = useAuth();

  const handleLogout = async () => {
    try {
      await signOut();
      message.success("Successfully logged out");
      router.push("/signin");
    } catch (error) {
      message.error("Failed to logout");
    }
  };

  const userMenu = (
    <Menu>
      <Menu.Item 
        key="profile" 
        icon={<UserOutlined />}
        onClick={() => router.push("/dashboard/profile")}
      >
        Profile
      </Menu.Item>
      <Menu.Item 
        key="settings" 
        icon={<SettingOutlined />}
        onClick={() => router.push("/dashboard/settings")}
      >
        Settings
      </Menu.Item>
      <Menu.Divider />
      <Menu.Item 
        key="logout" 
        icon={<LogoutOutlined />}
        onClick={handleLogout}
        danger
      >
        Logout
      </Menu.Item>
    </Menu>
  );

  return (
    <Header 
      className="fixed top-0 w-full z-10 flex justify-between items-center bg-white border-b px-6"
      style={{ height: '64px' }}
    >
      <div className="flex items-center">
        <h1 className="text-lg font-semibold m-0">Process Analysis Dashboard</h1>
      </div>

      <div className="flex items-center">
        <Dropdown overlay={userMenu} trigger={["click"]}>
          <Button type="text" className="flex items-center">
            <Avatar size="small" icon={<UserOutlined />} className="mr-2" />
            <span>{user?.name || "User"}</span>
          </Button>
        </Dropdown>
      </div>
    </Header>
  );
} 
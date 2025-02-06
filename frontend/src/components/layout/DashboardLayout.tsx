"use client";

import React, { useState } from "react";
import { Layout } from "antd";
import TopNav from "./TopNav";
import SideNav from "./SideNav";

const { Content } = Layout;

interface DashboardLayoutProps {
  children: React.ReactNode;
}

export default function DashboardLayout({ children }: DashboardLayoutProps) {
  return (
    <Layout className="min-h-screen">
      <TopNav />
      <Layout>
        <SideNav />
        <Layout>
          <Content
            className="p-6 overflow-auto transition-all duration-200"
            style={{
              marginTop: '64px',
              marginLeft: '250px', // This will be adjusted by CSS based on collapsed state
              minHeight: 'calc(100vh - 64px)',
              backgroundColor: '#fff'
            }}
          >
            {children}
          </Content>
        </Layout>
      </Layout>
    </Layout>
  );
}

"use client";

import React from "react";
import { Card, Row, Col, Progress, List, Tag } from "antd";
import {
  ExperimentOutlined,
  DollarOutlined,
  EnvironmentOutlined,
} from "@ant-design/icons";

interface AnalysisOverview {
  title: string;
  icon: React.ReactNode;
  color: string;
  total: number;
  completed: number;
  inProgress: number;
}

const analysisOverviews: AnalysisOverview[] = [
  {
    title: "Technical Analysis",
    icon: <ExperimentOutlined style={{ fontSize: "24px" }} />,
    color: "#1890ff",
    total: 27,
    completed: 24,
    inProgress: 3,
  },
  {
    title: "Economic Analysis",
    icon: <DollarOutlined style={{ fontSize: "24px" }} />,
    color: "#52c41a",
    total: 20,
    completed: 18,
    inProgress: 2,
  },
  {
    title: "Environmental Analysis",
    icon: <EnvironmentOutlined style={{ fontSize: "24px" }} />,
    color: "#722ed1",
    total: 19,
    completed: 15,
    inProgress: 4,
  },
];

const recentAnalyses = [
  {
    id: "1",
    name: "Protein Extraction Process",
    type: "technical",
    date: "2024-01-30",
    progress: 92,
    status: "Complete",
  },
  {
    id: "2",
    name: "Cost Analysis Q1 2024",
    type: "economic",
    date: "2024-01-29",
    progress: 68,
    status: "Complete",
  },
  {
    id: "3",
    name: "Carbon Footprint Assessment",
    type: "environmental",
    date: "2024-01-28",
    progress: 73,
    status: "In Progress",
  },
];

export default function DashboardPage() {
  return (
    <div>
      {/* Analysis Overview Cards */}
      <Row gutter={[16, 16]} className="mb-6">
        {analysisOverviews.map((analysis) => (
          <Col xs={24} md={8} key={analysis.title}>
            <Card bordered={false}>
              <div className="mb-4">
                <span
                  className="inline-flex items-center justify-center w-10 h-10 rounded-lg"
                  style={{ backgroundColor: `${analysis.color}20` }}
                >
                  <span style={{ color: analysis.color }}>{analysis.icon}</span>
                </span>
              </div>
              <div className="mb-2">
                <h3 className="text-lg font-medium">{analysis.title}</h3>
                <div className="text-3xl font-semibold mt-2">
                  {analysis.total}
                </div>
              </div>
              <Progress
                percent={Math.round(
                  (analysis.completed / analysis.total) * 100
                )}
                strokeColor={analysis.color}
                className="mb-2"
              />
              <div className="text-sm text-gray-500">
                {analysis.completed} Completed • {analysis.inProgress} In Progress
              </div>
            </Card>
          </Col>
        ))}
      </Row>

      {/* Recent Analyses */}
      <Card title="Recently Performed Analyses" bordered={false}>
        <List
          dataSource={recentAnalyses}
          renderItem={(item) => (
            <List.Item
              key={item.id}
              extra={
                <Tag
                  color={item.status === "Complete" ? "success" : "processing"}
                  className="ml-4"
                >
                  {item.status}
                </Tag>
              }
            >
              <List.Item.Meta
                avatar={
                  <span
                    className="inline-flex items-center justify-center w-8 h-8 rounded-full"
                    style={{
                      backgroundColor:
                        item.type === "technical"
                          ? "#1890ff20"
                          : item.type === "economic"
                          ? "#52c41a20"
                          : "#722ed120",
                    }}
                  >
                    {item.type === "technical" && "🔬"}
                    {item.type === "economic" && "💰"}
                    {item.type === "environmental" && "🌍"}
                  </span>
                }
                title={item.name}
                description={item.date}
              />
              <Progress
                percent={item.progress}
                size="small"
                status={item.status === "Complete" ? "success" : "active"}
                style={{ width: 180 }}
              />
            </List.Item>
          )}
        />
      </Card>
    </div>
  );
} 
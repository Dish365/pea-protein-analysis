"use client";

import React from "react";
import { Card, Table, Tag, Button, Spin, Alert, Tooltip } from "antd";
import { useRouter } from "next/navigation";
import { ProcessType, ProcessStatus } from "@/types/process";
import { useRecentAnalyses, Analysis } from "@/hooks/useRecentAnalyses";
import { formatDistanceToNow } from "date-fns";
import { ColumnsType } from "antd/es/table";
import type { Key } from "react";

const statusColors = {
  pending: "default",
  processing: "processing",
  completed: "success",
  failed: "error",
};

const RecentAnalyses: React.FC = () => {
  const router = useRouter();
  const { data, isLoading, isError, error } = useRecentAnalyses();

  const columns: ColumnsType<Analysis> = [
    {
      title: "Analysis Type",
      dataIndex: "type",
      key: "type",
      render: (type: ProcessType) => {
        const colors = {
          [ProcessType.RF]: "#1890ff",
          [ProcessType.IR]: "#52c41a",
          [ProcessType.BASELINE]: "#722ed1",
        };
        return <Tag color={colors[type]}>{type}</Tag>;
      },
      filters: [
        { text: "RF", value: ProcessType.RF },
        { text: "IR", value: ProcessType.IR },
        { text: "Baseline", value: ProcessType.BASELINE },
      ],
      onFilter: (value: Key | boolean, record: Analysis) =>
        record.type === value.toString(),
    },
    {
      title: "Status",
      dataIndex: "status",
      key: "status",
      render: (status: ProcessStatus) => (
        <Tag color={statusColors[status]}>
          {status.charAt(0).toUpperCase() + status.slice(1)}
        </Tag>
      ),
      filters: [
        { text: "Completed", value: "completed" },
        { text: "Processing", value: "processing" },
        { text: "Failed", value: "failed" },
        { text: "Pending", value: "pending" },
      ],
      onFilter: (value: Key | boolean, record: Analysis) =>
        record.status === value.toString(),
    },
    {
      title: "Started",
      dataIndex: "startedAt",
      key: "startedAt",
      render: (date: string) => (
        <Tooltip title={new Date(date).toLocaleString()}>
          {formatDistanceToNow(new Date(date), { addSuffix: true })}
        </Tooltip>
      ),
      sorter: (a: Analysis, b: Analysis) =>
        new Date(a.startedAt).getTime() - new Date(b.startedAt).getTime(),
    },
    {
      title: "Completed",
      dataIndex: "completedAt",
      key: "completedAt",
      render: (date?: string) =>
        date ? (
          <Tooltip title={new Date(date).toLocaleString()}>
            {formatDistanceToNow(new Date(date), { addSuffix: true })}
          </Tooltip>
        ) : (
          "-"
        ),
      sorter: (a: Analysis, b: Analysis) => {
        if (!a.completedAt) return 1;
        if (!b.completedAt) return -1;
        return (
          new Date(a.completedAt).getTime() - new Date(b.completedAt).getTime()
        );
      },
    },
    {
      title: "Action",
      key: "action",
      render: (record: Analysis) => (
        <Button
          type="link"
          onClick={() => router.push(`/analysis/${record.id}`)}
        >
          View Details
        </Button>
      ),
    },
  ];

  if (isLoading) {
    return (
      <div style={{ textAlign: "center", padding: "50px" }}>
        <Spin size="large" />
      </div>
    );
  }

  if (isError) {
    return (
      <Card title="Recent Analyses" className="mb-6">
        <Alert
          message="Error"
          description={error?.message || "Failed to load recent analyses"}
          type="error"
          showIcon
        />
      </Card>
    );
  }

  return (
    <Card
      title="Recent Analyses"
      className="mb-6"
      extra={
        <Button type="link" onClick={() => router.push("/analysis/history")}>
          View All
        </Button>
      }
    >
      <Table
        columns={columns}
        dataSource={data}
        rowKey="id"
        pagination={{ pageSize: 5 }}
        onChange={(pagination, filters, sorter) => {
          // Handle table changes if needed
          console.log("Table changed:", { pagination, filters, sorter });
        }}
      />
    </Card>
  );
};

export default RecentAnalyses;

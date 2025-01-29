"use client";

import React from 'react';
import { Card, Table, Tag, Button, Alert, Tooltip, Space } from 'antd';
import { useRouter } from 'next/navigation';
import { ProcessType, ProcessStatus } from '@/types/process';
import { useRecentAnalyses, Analysis } from '@/hooks/useRecentAnalyses';
import { formatDistanceToNow } from 'date-fns';
import { EyeOutlined, ReloadOutlined } from '@ant-design/icons';
import type { ColumnsType } from 'antd/es/table';
import type { Key } from 'react';

const statusConfig = {
  [ProcessStatus.PENDING]: {
    color: 'default',
    label: 'Pending'
  },
  [ProcessStatus.PROCESSING]: {
    color: 'processing',
    label: 'Processing'
  },
  [ProcessStatus.COMPLETED]: {
    color: 'success',
    label: 'Completed'
  },
  [ProcessStatus.FAILED]: {
    color: 'error',
    label: 'Failed'
  },
} as const;

const processTypeConfig = {
  [ProcessType.RF]: {
    color: '#1890ff',
    label: 'RF Process'
  },
  [ProcessType.IR]: {
    color: '#52c41a',
    label: 'IR Process'
  },
  [ProcessType.BASELINE]: {
    color: '#722ed1',
    label: 'Baseline'
  },
} as const;

const RecentAnalyses: React.FC = () => {
  const router = useRouter();
  const { data: queryData, isLoading, isError, error, refetch } = useRecentAnalyses();

  const columns: ColumnsType<Analysis> = [
    {
      title: 'Analysis Type',
      dataIndex: 'type',
      key: 'type',
      render: (type: ProcessType) => (
        <Tag color={processTypeConfig[type].color}>
          {processTypeConfig[type].label}
        </Tag>
      ),
      filters: Object.entries(processTypeConfig).map(([value, config]) => ({
        text: config.label,
        value,
      })),
      onFilter: (value: Key | boolean, record: Analysis) =>
        record.type === value.toString(),
    },
    {
      title: 'Status',
      dataIndex: 'status',
      key: 'status',
      render: (status: ProcessStatus) => (
        <Tag color={statusConfig[status].color}>
          {statusConfig[status].label}
        </Tag>
      ),
      filters: Object.entries(statusConfig).map(([value, config]) => ({
        text: config.label,
        value,
      })),
      onFilter: (value: Key | boolean, record: Analysis) =>
        record.status === value.toString(),
    },
    {
      title: 'Started',
      dataIndex: 'startedAt',
      key: 'startedAt',
      render: (date: string) => (
        <Tooltip title={new Date(date).toLocaleString()}>
          {formatDistanceToNow(new Date(date), { addSuffix: true })}
        </Tooltip>
      ),
      sorter: (a: Analysis, b: Analysis) =>
        new Date(a.startedAt).getTime() - new Date(b.startedAt).getTime(),
    },
    {
      title: 'Completed',
      dataIndex: 'completedAt',
      key: 'completedAt',
      render: (date?: string) =>
        date ? (
          <Tooltip title={new Date(date).toLocaleString()}>
            {formatDistanceToNow(new Date(date), { addSuffix: true })}
          </Tooltip>
        ) : '-',
      sorter: (a: Analysis, b: Analysis) => {
        if (!a.completedAt) return 1;
        if (!b.completedAt) return -1;
        return (
          new Date(a.completedAt).getTime() - new Date(b.completedAt).getTime()
        );
      },
    },
    {
      title: 'Action',
      key: 'action',
      render: (_: unknown, record: Analysis) => (
        <Button
          type="link"
          icon={<EyeOutlined />}
          onClick={() => router.push(`/analysis/${record.id}`)}
        >
          View Details
        </Button>
      ),
    },
  ];

  if (isError) {
    return (
      <Card title="Recent Analyses" className="mb-6">
        <Alert
          message="Error Loading Analyses"
          description={error instanceof Error ? error.message : 'Failed to load recent analyses'}
          type="error"
          showIcon
          action={
            <Button onClick={() => refetch()} icon={<ReloadOutlined />}>
              Retry
            </Button>
          }
        />
      </Card>
    );
  }

  return (
    <Card 
      title={
        <Space>
          Recent Analyses
          <Button 
            type="text" 
            icon={<ReloadOutlined />} 
            onClick={() => refetch()}
            size="small"
          />
        </Space>
      }
      className="mb-6"
      extra={
        <Button type="link" onClick={() => router.push('/analysis/history')}>
          View All
        </Button>
      }
    >
      <Table<Analysis>
        columns={columns}
        dataSource={queryData?.data}
        rowKey="id"
        pagination={{ 
          pageSize: 5,
          showTotal: (total) => `Total ${total} analyses`,
          total: queryData?.total
        }}
        loading={isLoading}
        onChange={(pagination, filters, sorter) => {
          console.log('Table changed:', { pagination, filters, sorter });
        }}
      />
    </Card>
  );
};

export default RecentAnalyses;

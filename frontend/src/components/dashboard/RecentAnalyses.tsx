"use client";

import React from 'react';
import { Card, List, Tag, Button, Space, Progress } from 'antd';
import { useRouter } from 'next/navigation';
import { ProcessType, ProcessStatus } from '@/types/process';
import { useRecentAnalyses } from '@/hooks/useRecentAnalyses';
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
  const { data: analyses, isLoading, error, refetch } = useRecentAnalyses();

  if (error) {
    return (
      <Card title="Recent Analyses">
        <div className="text-red-500">Failed to load recent analyses</div>
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
      loading={isLoading}
    >
      <List
        dataSource={analyses || []}
        renderItem={(analysis) => (
          <List.Item
            key={analysis.id}
            className="flex items-center justify-between"
            actions={[
              <Button
                key="view"
                type="link"
                onClick={() => router.push(`/analysis/${analysis.id}`)}
              >
                View Details
              </Button>,
            ]}
            extra={
              <Progress 
                percent={analysis.progress} 
                status={analysis.status === "completed" ? "success" : "active"}
              />
            }
          >
            <div className="flex items-center">
              <div className="mr-4">
                {analysis.type === "technical" && "🔬"}
                {analysis.type === "economic" && "💰"}
                {analysis.type === "environmental" && "🌍"}
              </div>
              <div>
                <div className="font-medium">
                  {analysis.type.charAt(0).toUpperCase() + analysis.type.slice(1)} Analysis
                </div>
                <div className="text-sm text-gray-500">
                  {formatDistanceToNow(new Date(analysis.date), { addSuffix: true })}
                </div>
              </div>
            </div>
            <Tag color={analysis.status === "completed" ? "success" : "processing"}>
              {analysis.status}
            </Tag>
          </List.Item>
        )}
      />
    </Card>
  );
};

export default RecentAnalyses;

import React from 'react';
import { Card, Statistic, Button, Progress, Tooltip } from 'antd';
import { ArrowUpOutlined, ArrowDownOutlined } from '@ant-design/icons';

interface AnalysisCardProps {
  title: string;
  description: string;
  icon: React.ReactNode;
  color: string;
  metrics: {
    completed: number;
    inProgress: number;
    trend?: number; // Percentage change from last period
  };
  onClick: () => void;
}

const AnalysisCard: React.FC<AnalysisCardProps> = ({
  title,
  description,
  icon,
  color,
  metrics,
  onClick,
}) => {
  const totalAnalyses = metrics.completed + metrics.inProgress;
  const completionRate = (metrics.completed / totalAnalyses) * 100;

  return (
    <Card
      hoverable
      className="h-full"
      style={{ borderTop: `2px solid ${color}` }}
    >
      <div className="flex items-start mb-4">
        <div
          className="p-2 rounded-lg mr-4"
          style={{ backgroundColor: `${color}20` }}
        >
          {icon}
        </div>
        <div>
          <h2 className="text-lg font-semibold">{title}</h2>
          <p className="text-gray-600">{description}</p>
        </div>
      </div>

      <div className="mb-4">
        <Tooltip title="Analysis completion rate">
          <Progress
            percent={Math.round(completionRate)}
            strokeColor={color}
            size="small"
          />
        </Tooltip>
      </div>

      <div className="grid grid-cols-2 gap-4 mb-4">
        <Statistic
          title="Completed"
          value={metrics.completed}
          valueStyle={{ color }}
        />
        <Statistic
          title="In Progress"
          value={metrics.inProgress}
          valueStyle={{ color: '#faad14' }}
        />
      </div>

      {metrics.trend !== undefined && (
        <div className="mb-4">
          <Statistic
            title="Trend"
            value={metrics.trend}
            precision={1}
            valueStyle={{ color: metrics.trend > 0 ? '#3f8600' : '#cf1322' }}
            prefix={metrics.trend > 0 ? <ArrowUpOutlined /> : <ArrowDownOutlined />}
            suffix="%"
          />
        </div>
      )}

      <Button
        type="primary"
        block
        onClick={onClick}
        style={{ backgroundColor: color }}
      >
        Start New Analysis
      </Button>
    </Card>
  );
};

export default AnalysisCard; 
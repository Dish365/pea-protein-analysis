import React from 'react';
import { Spin, Progress, Typography } from 'antd';
import { LoadingOutlined } from '@ant-design/icons';
import clsx from 'clsx';

const { Text } = Typography;

interface LoadingSpinnerProps {
  tip?: string;
  subTip?: string;
  progress?: number;
  size?: 'small' | 'default' | 'large';
  fullscreen?: boolean;
  className?: string;
}

const LoadingSpinner: React.FC<LoadingSpinnerProps> = ({ 
  tip = 'Loading...', 
  subTip,
  progress,
  size = 'default',
  fullscreen = false,
  className 
}) => {
  const spinSize = {
    small: 16,
    default: 24,
    large: 36
  }[size];

  return (
    <div className={clsx(
      'flex flex-col items-center justify-center gap-4',
      fullscreen && 'fixed inset-0 bg-white/80 z-50',
      !fullscreen && 'p-8',
      className
    )}>
      <Spin 
        size={size}
        indicator={<LoadingOutlined style={{ fontSize: spinSize }} spin />} 
      />
      <Text strong style={{ fontSize: size === 'large' ? '16px' : '14px' }}>
        {tip}
      </Text>
      {progress !== undefined && (
        <Progress 
          percent={progress} 
          status="active"
          size={size === 'small' ? 'small' : 'default'}
          style={{ width: size === 'large' ? '200px' : '160px' }}
        />
      )}
      {subTip && (
        <Text type="secondary" className="text-sm">
          {subTip}
        </Text>
      )}
    </div>
  );
};

export default LoadingSpinner; 
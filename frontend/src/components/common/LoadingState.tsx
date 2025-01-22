"use client";

import React from 'react';
import { Spin, Progress, Typography } from 'antd';
import { LoadingOutlined } from '@ant-design/icons';

const { Text } = Typography;

interface LoadingStateProps {
  tip?: string;
  progress?: number;
  subTip?: string;
}

const LoadingState: React.FC<LoadingStateProps> = ({ 
  tip = "Loading...", 
  progress, 
  subTip 
}) => {
  return (
    <div className="loading-container" style={{ 
      textAlign: 'center', 
      padding: '40px',
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      gap: '16px'
    }}>
      <Spin 
        size="large" 
        indicator={<LoadingOutlined style={{ fontSize: 36 }} spin />}
      />
      <Text strong style={{ fontSize: '16px' }}>{tip}</Text>
      {progress !== undefined && (
        <Progress 
          percent={progress} 
          status="active"
          style={{ width: '200px' }}
        />
      )}
      {subTip && (
        <Text type="secondary">{subTip}</Text>
      )}
    </div>
  );
};

export default LoadingState; 
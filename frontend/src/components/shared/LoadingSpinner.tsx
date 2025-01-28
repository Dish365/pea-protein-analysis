import React from 'react';
import { Spin } from 'antd';
import { LoadingOutlined } from '@ant-design/icons';
import clsx from 'clsx';

interface LoadingSpinnerProps {
  tip?: string;
  className?: string;
}

const LoadingSpinner: React.FC<LoadingSpinnerProps> = ({ 
  tip = 'Loading...', 
  className 
}) => {
  return (
    <div className={clsx(
      'flex flex-col items-center justify-center p-8',
      className
    )}>
      <Spin 
        indicator={<LoadingOutlined style={{ fontSize: 24 }} spin />} 
        tip={tip}
      />
    </div>
  );
};

export default LoadingSpinner; 
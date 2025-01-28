import React from 'react';
import { Card as AntCard } from 'antd';
import type { CardProps as AntCardProps } from 'antd';
import clsx from 'clsx';

interface CardProps extends AntCardProps {
  className?: string;
  elevated?: boolean;
  noPadding?: boolean;
}

const Card: React.FC<CardProps> = ({ 
  className, 
  children, 
  elevated = false,
  noPadding = false,
  ...props 
}) => {
  return (
    <AntCard
      className={clsx(
        elevated && 'shadow-md hover:shadow-lg transition-shadow duration-200',
        !elevated && 'shadow-sm',
        noPadding && '!p-0',
        className
      )}
      {...props}
    >
      {children}
    </AntCard>
  );
};

export default Card; 
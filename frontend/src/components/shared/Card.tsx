import React from 'react';
import { Card as AntCard } from 'antd';
import type { CardProps as AntCardProps } from 'antd';
import clsx from 'clsx';

interface CardProps extends AntCardProps {
  className?: string;
}

export const Card: React.FC<CardProps> = ({ className, children, ...props }) => {
  return (
    <AntCard
      className={clsx('card-shadow', className)}
      {...props}
    >
      {children}
    </AntCard>
  );
};

export default Card; 
import React from 'react';
import { Modal, Spin, Progress, Typography } from 'antd';
import { LoadingOutlined } from '@ant-design/icons';
import clsx from 'clsx';

const { Text } = Typography;

interface LoadingOverlayProps {
  visible: boolean;
  title?: string;
  description?: string;
  progress?: number;
  className?: string;
}

const LoadingOverlay: React.FC<LoadingOverlayProps> = ({
  visible,
  title = 'Processing...',
  description,
  progress,
  className
}) => {
  return (
    <Modal
      open={visible}
      closable={false}
      footer={null}
      centered
      maskClosable={false}
      className={clsx('loading-overlay-modal', className)}
      width={400}
    >
      <div className="flex flex-col items-center gap-6 py-8">
        <Spin
          size="large"
          indicator={<LoadingOutlined style={{ fontSize: 40 }} spin />}
        />
        <div className="text-center">
          <Text strong className="text-lg block mb-2">
            {title}
          </Text>
          {description && (
            <Text type="secondary" className="block">
              {description}
            </Text>
          )}
        </div>
        {progress !== undefined && (
          <Progress
            percent={progress}
            status="active"
            strokeWidth={8}
            style={{ width: '100%' }}
          />
        )}
      </div>
    </Modal>
  );
};

export default LoadingOverlay; 
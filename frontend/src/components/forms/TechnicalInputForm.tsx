"use client";

import React from 'react';
import { Form, Input, Select, Button, Tooltip, Space, Card } from 'antd';
import { PROCESS_TYPES, DEFAULT_PROCESS_ANALYSIS } from '@/config/constants';
import { TechnicalParameters } from '@/types/technical';
import { formatNumber } from '@/lib/formatters';
import { InfoCircleOutlined } from '@ant-design/icons';

interface TechnicalInputFormProps {
  onSubmit: (values: TechnicalParameters) => void;
  isSubmitting: boolean;
}

export default function TechnicalInputForm({ onSubmit, isSubmitting }: TechnicalInputFormProps) {
  const [form] = Form.useForm();

  return (
    <Form
      form={form}
      layout="vertical"
      initialValues={DEFAULT_PROCESS_ANALYSIS}
      onFinish={onSubmit}
    >
      <Card title="Process Configuration" className="mb-6">
        <Form.Item
          label="Process Type"
          name="processType"
          rules={[{ required: true, message: 'Please select process type' }]}
        >
          <Select options={PROCESS_TYPES} />
        </Form.Item>

        <Form.Item
          label={
            <Space>
              Air Flow Rate (m³/h)
              <Tooltip title="Recommended range: 400-600 m³/h">
                <InfoCircleOutlined />
              </Tooltip>
            </Space>
          }
          name="airFlowRate"
          rules={[{ required: true, message: 'Please input air flow rate' }]}
        >
          <Input type="number" />
        </Form.Item>
      </Card>

      <Card title="Process Parameters" className="mb-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <Form.Item
            label="Temperature (°C)"
            name="temperature"
            rules={[{ required: true }]}
          >
            <Input type="number" />
          </Form.Item>

          <Form.Item
            label="Pressure (bar)"
            name="pressure"
            rules={[{ required: true }]}
          >
            <Input type="number" />
          </Form.Item>
        </div>
      </Card>

      <Card title="Mass & Content Analysis">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <Form.Item
            label="Input Mass (kg)"
            name="inputMass"
            rules={[{ required: true }]}
          >
            <Input type="number" />
          </Form.Item>

          <Form.Item
            label="Output Mass (kg)"
            name="outputMass"
            rules={[{ required: true }]}
          >
            <Input type="number" />
          </Form.Item>

          <Form.Item
            label="Initial Protein Content (%)"
            name="initialProteinContent"
            rules={[{ required: true }]}
          >
            <Input type="number" />
          </Form.Item>

          <Form.Item
            label="Target Protein Content (%)"
            name="targetProteinContent"
            rules={[{ required: true }]}
          >
            <Input type="number" />
          </Form.Item>
        </div>
      </Card>

      <div className="flex justify-end mt-6">
        <Space>
          <Button onClick={() => form.resetFields()}>
            Reset
          </Button>
          <Button type="primary" htmlType="submit" loading={isSubmitting}>
            Analyze
          </Button>
        </Space>
      </div>
    </Form>
  );
}

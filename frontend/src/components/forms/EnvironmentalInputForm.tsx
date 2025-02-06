"use client";

import React from 'react';
import { Form, Input, Select, Button, Tooltip, Space, Card } from 'antd';
import { PROCESS_TYPES } from '@/config/constants';
import { EnvironmentalParameters } from '@/types/environmental';
import { formatNumber } from '@/lib/formatters';
import { InfoCircleOutlined } from '@ant-design/icons';

interface EnvironmentalInputFormProps {
  onSubmit: (values: EnvironmentalParameters) => void;
  isSubmitting: boolean;
}

export default function EnvironmentalInputForm({ onSubmit, isSubmitting }: EnvironmentalInputFormProps) {
  const [form] = Form.useForm();

  return (
    <Form
      form={form}
      layout="vertical"
      onFinish={onSubmit}
    >
      <Card title="Process Information" className="mb-6">
        <Form.Item
          label="Process Type"
          name="processType"
          rules={[{ required: true }]}
        >
          <Select options={PROCESS_TYPES} />
        </Form.Item>

        <Form.Item
          label="Production Volume (kg/year)"
          name="productionVolume"
          rules={[{ required: true }]}
        >
          <Input type="number" />
        </Form.Item>
      </Card>

      <Card title="Resource Consumption" className="mb-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <Form.Item
            label="Electricity Consumption (kWh/kg)"
            name="electricityConsumption"
            rules={[{ required: true }]}
          >
            <Input type="number" />
          </Form.Item>

          <Form.Item
            label="Water Consumption (L/kg)"
            name="waterConsumption"
            rules={[{ required: true }]}
          >
            <Input type="number" />
          </Form.Item>

          <Form.Item
            label="Natural Gas Consumption (m³/kg)"
            name="naturalGasConsumption"
            rules={[{ required: true }]}
          >
            <Input type="number" />
          </Form.Item>

          <Form.Item
            label="Waste Generation (kg/kg product)"
            name="wasteGeneration"
            rules={[{ required: true }]}
          >
            <Input type="number" />
          </Form.Item>
        </div>
      </Card>

      <Card title="Transport & Packaging">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <Form.Item
            label="Transport Distance (km)"
            name="transportDistance"
            rules={[{ required: true }]}
          >
            <Input type="number" />
          </Form.Item>

          <Form.Item
            label="Packaging Material"
            name="packagingMaterial"
            rules={[{ required: true }]}
          >
            <Select
              options={[
                { value: 'plastic', label: 'Plastic' },
                { value: 'paper', label: 'Paper' },
                { value: 'composite', label: 'Composite' },
              ]}
            />
          </Form.Item>

          <Form.Item
            label="Recycled Content (%)"
            name="recycledContent"
            rules={[{ required: true }]}
          >
            <Input type="number" suffix="%" />
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

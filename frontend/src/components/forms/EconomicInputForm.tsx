"use client";

import React from 'react';
import { Form, Input, Select, Button, Tooltip, Space, Card } from 'antd';
import { PROCESS_TYPES } from '@/config/constants';
import { EconomicParameters } from '@/types/economic';
import { formatNumber, formatCurrency } from '@/lib/formatters';
import { InfoCircleOutlined } from '@ant-design/icons';

interface EconomicInputFormProps {
  onSubmit: (values: EconomicParameters) => void;
  isSubmitting: boolean;
}

export default function EconomicInputForm({ onSubmit, isSubmitting }: EconomicInputFormProps) {
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

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <Form.Item
            label="Production Volume (kg/year)"
            name="productionVolume"
            rules={[{ required: true }]}
          >
            <Input type="number" />
          </Form.Item>

          <Form.Item
            label="Operating Hours (h/year)"
            name="operatingHours"
            rules={[{ required: true }]}
          >
            <Input type="number" />
          </Form.Item>
        </div>
      </Card>

      <Card title="Cost Factors" className="mb-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <Form.Item
            label={
              <Space>
                Equipment Cost
                <Tooltip title="Total cost of processing equipment">
                  <InfoCircleOutlined />
                </Tooltip>
              </Space>
            }
            name="equipmentCost"
            rules={[{ required: true }]}
          >
            <Input type="number" prefix="$" />
          </Form.Item>

          <Form.Item
            label="Utility Rate ($/kWh)"
            name="utilityRate"
            rules={[{ required: true }]}
          >
            <Input type="number" prefix="$" />
          </Form.Item>

          <Form.Item
            label="Raw Material Cost ($/kg)"
            name="rawMaterialCost"
            rules={[{ required: true }]}
          >
            <Input type="number" prefix="$" />
          </Form.Item>

          <Form.Item
            label="Labor Rate ($/h)"
            name="laborRate"
            rules={[{ required: true }]}
          >
            <Input type="number" prefix="$" />
          </Form.Item>
        </div>
      </Card>

      <Card title="Cost Factors">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <Form.Item
            label={
              <Space>
                Maintenance Factor (%)
                <Tooltip title="Percentage of equipment cost">
                  <InfoCircleOutlined />
                </Tooltip>
              </Space>
            }
            name="maintenanceFactor"
            rules={[{ required: true }]}
          >
            <Input type="number" suffix="%" />
          </Form.Item>

          <Form.Item
            label={
              <Space>
                Indirect Cost Factor (%)
                <Tooltip title="Percentage of direct costs">
                  <InfoCircleOutlined />
                </Tooltip>
              </Space>
            }
            name="indirectCostFactor"
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

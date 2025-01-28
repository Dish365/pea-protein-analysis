"use client";

import React from 'react';
import { Form, InputNumber, Row, Col, Card, Button, Tooltip, Space } from 'antd';
import { InfoCircleOutlined } from '@ant-design/icons';
import { formatCurrency, formatPercentage, formatNumber } from '@/lib/formatters';
import { DEFAULT_PROCESS_ANALYSIS } from '@/config/constants';
import { EconomicParameters } from '@/types/economic';

interface EconomicInputFormProps {
  onSubmit: (values: EconomicParameters) => Promise<void>;
  isSubmitting?: boolean;
  initialValues?: Partial<EconomicParameters>;
}

const EconomicInputForm: React.FC<EconomicInputFormProps> = ({
  onSubmit,
  isSubmitting = false,
  initialValues = DEFAULT_PROCESS_ANALYSIS,
}) => {
  const [form] = Form.useForm<EconomicParameters>();

  // Helper function for form item tooltip
  const FormLabel = ({ label, tooltip }: { label: string; tooltip: string }) => (
    <Space>
      {label}
      <Tooltip title={tooltip}>
        <InfoCircleOutlined style={{ color: '#1890ff' }} />
      </Tooltip>
    </Space>
  );

  return (
    <Form
      form={form}
      layout="vertical"
      onFinish={onSubmit}
      initialValues={initialValues}
      className="max-w-4xl mx-auto"
    >
      <Card title="Capital Costs" className="mb-6 shadow-sm">
        <Row gutter={16}>
          <Col span={12}>
            <Form.Item
              name="equipment_cost"
              label={
                <FormLabel 
                  label="Equipment Cost ($)" 
                  tooltip="Total cost of process equipment including installation"
                />
              }
              rules={[{ required: true, type: 'number', min: 0 }]}
            >
              <InputNumber
                min={0}
                step={1000}
                formatter={(value) => formatCurrency(value as number)}
                parser={(value: string | undefined): number => value ? parseFloat(value.replace(/[^\d.]/g, '')) : 0}
                style={{ width: '100%' }}
                className="text-right"
              />
            </Form.Item>
          </Col>
          <Col span={12}>
            <Form.Item
              name="maintenance_cost"
              label={
                <FormLabel 
                  label="Annual Maintenance Cost ($)" 
                  tooltip="Yearly cost for equipment maintenance and repairs"
                />
              }
              rules={[{ required: true, type: 'number', min: 0 }]}
            >
              <InputNumber
                min={0}
                step={100}
                formatter={(value) => formatCurrency(value as number)}
                parser={(value: string | undefined): number => value ? parseFloat(value.replace(/[^\d.]/g, '')) : 0}
                style={{ width: '100%' }}
                className="text-right"
              />
            </Form.Item>
          </Col>
        </Row>

        <Row gutter={16} className="mt-4">
          <Col span={8}>
            <Form.Item
              name="installation_factor"
              label={
                <FormLabel 
                  label="Installation Factor" 
                  tooltip="Factor for installation costs as percentage of equipment cost"
                />
              }
              rules={[{ required: true, type: 'number', min: 0, max: 1 }]}
            >
              <InputNumber
                min={0}
                max={1}
                step={0.05}
                formatter={(value) => formatPercentage(value as number)}
                parser={(value: string | undefined): number => value ? parseFloat(value.replace(/[^0-9.]/g, '')) / 100 : 0}
                style={{ width: '100%' }}
                className="text-right"
              />
            </Form.Item>
          </Col>
          <Col span={8}>
            <Form.Item
              name="indirect_costs_factor"
              label={
                <FormLabel 
                  label="Indirect Costs Factor" 
                  tooltip="Factor for indirect costs as percentage of direct costs"
                />
              }
              rules={[{ required: true, type: 'number', min: 0, max: 1 }]}
            >
              <InputNumber
                min={0}
                max={1}
                step={0.05}
                formatter={(value) => formatPercentage(value as number)}
                parser={(value: string | undefined): number => value ? parseFloat(value.replace(/[^0-9.]/g, '')) / 100 : 0}
                style={{ width: '100%' }}
                className="text-right"
              />
            </Form.Item>
          </Col>
          <Col span={8}>
            <Form.Item
              name="maintenance_factor"
              label={
                <FormLabel 
                  label="Maintenance Factor" 
                  tooltip="Annual maintenance cost as percentage of equipment cost"
                />
              }
              rules={[{ required: true, type: 'number', min: 0, max: 1 }]}
            >
              <InputNumber
                min={0}
                max={1}
                step={0.05}
                formatter={(value) => formatPercentage(value as number)}
                parser={(value: string | undefined): number => value ? parseFloat(value.replace(/[^0-9.]/g, '')) / 100 : 0}
                style={{ width: '100%' }}
                className="text-right"
              />
            </Form.Item>
          </Col>
        </Row>
      </Card>

      <Card title="Operating Costs" className="mb-6 shadow-sm">
        <Row gutter={16}>
          <Col span={8}>
            <Form.Item
              name="raw_material_cost"
              label={
                <FormLabel 
                  label="Raw Material Cost ($/kg)" 
                  tooltip="Cost per kilogram of input material"
                />
              }
              rules={[{ required: true, type: 'number', min: 0 }]}
            >
              <InputNumber
                min={0}
                step={0.1}
                formatter={(value) => formatCurrency(value as number)}
                parser={(value: string | undefined): number => value ? parseFloat(value.replace(/[^\d.]/g, '')) : 0}
                style={{ width: '100%' }}
                className="text-right"
              />
            </Form.Item>
          </Col>
          <Col span={8}>
            <Form.Item
              name="utility_cost"
              label={
                <FormLabel 
                  label="Utility Cost ($/kWh)" 
                  tooltip="Average cost per kilowatt-hour of energy consumption"
                />
              }
              rules={[{ required: true, type: 'number', min: 0 }]}
            >
              <InputNumber
                min={0}
                step={0.01}
                formatter={(value) => formatCurrency(value as number)}
                parser={(value: string | undefined): number => value ? parseFloat(value.replace(/[^\d.]/g, '')) : 0}
                style={{ width: '100%' }}
                className="text-right"
              />
            </Form.Item>
          </Col>
          <Col span={8}>
            <Form.Item
              name="labor_cost"
              label={
                <FormLabel 
                  label="Labor Cost ($/year)" 
                  tooltip="Total annual labor cost including wages and benefits"
                />
              }
              rules={[{ required: true, type: 'number', min: 0 }]}
            >
              <InputNumber
                min={0}
                step={1000}
                formatter={(value) => formatCurrency(value as number)}
                parser={(value: string | undefined): number => value ? parseFloat(value.replace(/[^\d.]/g, '')) : 0}
                style={{ width: '100%' }}
                className="text-right"
              />
            </Form.Item>
          </Col>
        </Row>
      </Card>

      <Card title="Project Parameters" className="mb-6 shadow-sm">
        <Row gutter={16}>
          <Col span={8}>
            <Form.Item
              name="production_volume"
              label={
                <FormLabel 
                  label="Annual Production (kg/year)" 
                  tooltip="Expected yearly production volume"
                />
              }
              rules={[{ required: true, type: 'number', min: 0 }]}
            >
              <InputNumber
                min={0}
                step={100}
                formatter={(value) => formatNumber(value as number)}
                parser={(value: string | undefined): number => value ? parseFloat(value.replace(/[^\d.]/g, '')) : 0}
                style={{ width: '100%' }}
                className="text-right"
              />
            </Form.Item>
          </Col>
          <Col span={8}>
            <Form.Item
              name="revenue_per_year"
              label={
                <FormLabel 
                  label="Annual Revenue ($)" 
                  tooltip="Expected yearly revenue from product sales"
                />
              }
              rules={[{ required: true, type: 'number', min: 0 }]}
            >
              <InputNumber
                min={0}
                step={1000}
                formatter={(value) => formatCurrency(value as number)}
                parser={(value: string | undefined): number => value ? parseFloat(value.replace(/[^\d.]/g, '')) : 0}
                style={{ width: '100%' }}
                className="text-right"
              />
            </Form.Item>
          </Col>
          <Col span={8}>
            <Form.Item
              name="project_duration"
              label={
                <FormLabel 
                  label="Project Duration (years)" 
                  tooltip="Expected lifetime of the project"
                />
              }
              rules={[{ required: true, type: 'number', min: 1, max: 30 }]}
            >
              <InputNumber
                min={1}
                max={30}
                step={1}
                formatter={(value) => `${value} years`}
                parser={(value: string | undefined): number => value ? parseInt(value.replace(/[^\d]/g, '')) : 1}
                style={{ width: '100%' }}
                className="text-right"
              />
            </Form.Item>
          </Col>
        </Row>
        <Row gutter={16} className="mt-4">
          <Col span={12}>
            <Form.Item
              name="discount_rate"
              label={
                <FormLabel 
                  label="Discount Rate (%)" 
                  tooltip="Annual discount rate for NPV calculations"
                />
              }
              rules={[{ required: true, type: 'number', min: 0, max: 100 }]}
            >
              <InputNumber
                min={0}
                max={100}
                step={0.5}
                formatter={(value) => formatPercentage(value as number)}
                parser={(value: string | undefined): number => value ? parseFloat(value.replace(/[^0-9.]/g, '')) / 100 : 0}
                style={{ width: '100%' }}
                className="text-right"
              />
            </Form.Item>
          </Col>
        </Row>
      </Card>

      <div className="flex justify-end gap-4 mt-6">
        <Button 
          onClick={() => form.resetFields()} 
          disabled={isSubmitting}
        >
          Reset
        </Button>
        <Button
          type="primary"
          htmlType="submit"
          loading={isSubmitting}
          size="large"
        >
          Continue to Environmental Parameters
        </Button>
      </div>
    </Form>
  );
};

export default EconomicInputForm;

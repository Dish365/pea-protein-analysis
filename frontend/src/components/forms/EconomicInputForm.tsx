"use client";

import React from 'react';
import { Form, InputNumber, Row, Col, Card, Button } from 'antd';
import { formatCurrency } from '@/lib/formatters';

interface EconomicInputFormProps {
  onSubmit: (values: any) => Promise<void>;
  isSubmitting?: boolean;
}

const EconomicInputForm: React.FC<EconomicInputFormProps> = ({
  onSubmit,
  isSubmitting = false,
}) => {
  const [form] = Form.useForm();

  const handleSubmit = async (values: any) => {
    await onSubmit(values);
  };

  return (
    <Form
      form={form}
      layout="vertical"
      onFinish={handleSubmit}
      className="max-w-4xl mx-auto"
    >
      <Card title="Capital Costs" className="mb-6">
        <Row gutter={16}>
          <Col span={12}>
            <Form.Item
              name="equipment_cost"
              label="Equipment Cost"
              rules={[{ required: true, message: 'Please enter equipment cost' }]}
            >
              <InputNumber
                min={0}
                style={{ width: '100%' }}
                formatter={value => formatCurrency(Number(value))}
                parser={value => value!.replace(/\$\s?|(,*)/g, '')}
              />
            </Form.Item>
          </Col>
          <Col span={12}>
            <Form.Item
              name="maintenance_cost"
              label="Annual Maintenance Cost"
              rules={[{ required: true, message: 'Please enter maintenance cost' }]}
            >
              <InputNumber
                min={0}
                style={{ width: '100%' }}
                formatter={value => formatCurrency(Number(value))}
                parser={value => value!.replace(/\$\s?|(,*)/g, '')}
              />
            </Form.Item>
          </Col>
        </Row>
      </Card>

      <Card title="Operating Costs" className="mb-6">
        <Row gutter={16}>
          <Col span={8}>
            <Form.Item
              name="raw_material_cost"
              label="Raw Material Cost (per unit)"
              rules={[{ required: true, message: 'Please enter raw material cost' }]}
            >
              <InputNumber
                min={0}
                style={{ width: '100%' }}
                formatter={value => formatCurrency(Number(value))}
                parser={value => value!.replace(/\$\s?|(,*)/g, '')}
              />
            </Form.Item>
          </Col>
          <Col span={8}>
            <Form.Item
              name="utility_cost"
              label="Utility Cost (per unit)"
              rules={[{ required: true, message: 'Please enter utility cost' }]}
            >
              <InputNumber
                min={0}
                style={{ width: '100%' }}
                formatter={value => formatCurrency(Number(value))}
                parser={value => value!.replace(/\$\s?|(,*)/g, '')}
              />
            </Form.Item>
          </Col>
          <Col span={8}>
            <Form.Item
              name="labor_cost"
              label="Labor Cost (per year)"
              rules={[{ required: true, message: 'Please enter labor cost' }]}
            >
              <InputNumber
                min={0}
                style={{ width: '100%' }}
                formatter={value => formatCurrency(Number(value))}
                parser={value => value!.replace(/\$\s?|(,*)/g, '')}
              />
            </Form.Item>
          </Col>
        </Row>
      </Card>

      <Card title="Project Parameters" className="mb-6">
        <Row gutter={16}>
          <Col span={8}>
            <Form.Item
              name="production_volume"
              label="Annual Production Volume"
              rules={[{ required: true, message: 'Please enter production volume' }]}
            >
              <InputNumber min={0} style={{ width: '100%' }} />
            </Form.Item>
          </Col>
          <Col span={8}>
            <Form.Item
              name="selling_price"
              label="Selling Price (per unit)"
              rules={[{ required: true, message: 'Please enter selling price' }]}
            >
              <InputNumber
                min={0}
                style={{ width: '100%' }}
                formatter={value => formatCurrency(Number(value))}
                parser={value => value!.replace(/\$\s?|(,*)/g, '')}
              />
            </Form.Item>
          </Col>
          <Col span={8}>
            <Form.Item
              name="project_duration"
              label="Project Duration (years)"
              rules={[{ required: true, message: 'Please enter project duration' }]}
            >
              <InputNumber min={1} max={30} style={{ width: '100%' }} />
            </Form.Item>
          </Col>
        </Row>
        <Row gutter={16}>
          <Col span={12}>
            <Form.Item
              name="discount_rate"
              label="Discount Rate (%)"
              rules={[{ required: true, message: 'Please enter discount rate' }]}
            >
              <InputNumber
                min={0}
                max={100}
                step={0.1}
                style={{ width: '100%' }}
              />
            </Form.Item>
          </Col>
        </Row>
      </Card>

      <div className="flex justify-end mt-6">
        <Button
          type="primary"
          htmlType="submit"
          loading={isSubmitting}
          size="large"
        >
          Start Analysis
        </Button>
      </div>
    </Form>
  );
};

export default EconomicInputForm;

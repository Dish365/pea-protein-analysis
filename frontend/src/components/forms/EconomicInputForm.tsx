"use client";

import React from 'react';
import { Form, InputNumber, Row, Col, Card, Divider } from 'antd';
import { FormInstance } from 'antd/lib/form';

interface EconomicInputFormProps {
  form: FormInstance;
  onSuccess: (response: any) => Promise<void>;
  loading: boolean;
}

const EconomicInputForm: React.FC<EconomicInputFormProps> = ({ form }) => {
  return (
    <div className="economic-input-form">
      <Card title="Equipment Configuration">
        <Row gutter={16}>
          <Col span={12}>
            <Form.Item
              name={['equipment', 0, 'cost']}
              label="Equipment Cost (USD)"
              rules={[{ required: true, message: 'Please enter equipment cost' }]}
            >
              <InputNumber min={0} style={{ width: '100%' }} />
            </Form.Item>
          </Col>
          <Col span={12}>
            <Form.Item
              name={['equipment', 0, 'efficiency']}
              label="Equipment Efficiency"
              initialValue={0.85}
            >
              <InputNumber min={0} max={1} step={0.01} style={{ width: '100%' }} />
            </Form.Item>
          </Col>
        </Row>
        <Row gutter={16}>
          <Col span={12}>
            <Form.Item
              name={['equipment', 0, 'maintenance_cost']}
              label="Maintenance Cost (USD/year)"
              rules={[{ required: true, message: 'Please enter maintenance cost' }]}
            >
              <InputNumber min={0} style={{ width: '100%' }} />
            </Form.Item>
          </Col>
          <Col span={12}>
            <Form.Item
              name={['equipment', 0, 'processing_capacity']}
              label="Processing Capacity (kg/year)"
              rules={[{ required: true, message: 'Please enter processing capacity' }]}
            >
              <InputNumber min={0} style={{ width: '100%' }} />
            </Form.Item>
          </Col>
        </Row>
      </Card>

      <Divider />

      <Card title="Utilities Configuration">
        <Row gutter={16}>
          <Col span={8}>
            <Form.Item
              name={['utilities', 0, 'consumption']}
              label="Electricity Consumption (kWh)"
              rules={[{ required: true, message: 'Please enter electricity consumption' }]}
            >
              <InputNumber min={0} style={{ width: '100%' }} />
            </Form.Item>
          </Col>
          <Col span={8}>
            <Form.Item
              name={['utilities', 1, 'consumption']}
              label="Cooling Consumption (kWh)"
              rules={[{ required: true, message: 'Please enter cooling consumption' }]}
            >
              <InputNumber min={0} style={{ width: '100%' }} />
            </Form.Item>
          </Col>
          <Col span={8}>
            <Form.Item
              name={['utilities', 2, 'consumption']}
              label="Water Consumption (kg)"
              rules={[{ required: true, message: 'Please enter water consumption' }]}
            >
              <InputNumber min={0} style={{ width: '100%' }} />
            </Form.Item>
          </Col>
        </Row>
        <Row gutter={16}>
          <Col span={8}>
            <Form.Item
              name="utility_cost"
              label="Utility Unit Cost (USD/unit)"
              rules={[{ required: true, message: 'Please enter utility cost' }]}
            >
              <InputNumber min={0} style={{ width: '100%' }} />
            </Form.Item>
          </Col>
        </Row>
      </Card>

      <Divider />

      <Card title="Raw Materials">
        <Row gutter={16}>
          <Col span={12}>
            <Form.Item
              name="raw_material_cost"
              label="Raw Material Cost (USD/kg)"
              rules={[{ required: true, message: 'Please enter raw material cost' }]}
            >
              <InputNumber min={0} style={{ width: '100%' }} />
            </Form.Item>
          </Col>
        </Row>
      </Card>

      <Divider />

      <Card title="Labor Configuration">
        <Row gutter={16}>
          <Col span={12}>
            <Form.Item
              name={['labor_config', 'hourly_wage']}
              label="Hourly Wage (USD/hour)"
              rules={[{ required: true, message: 'Please enter hourly wage' }]}
            >
              <InputNumber min={0} style={{ width: '100%' }} />
            </Form.Item>
          </Col>
          <Col span={12}>
            <Form.Item
              name={['labor_config', 'num_workers']}
              label="Number of Workers"
              initialValue={1}
            >
              <InputNumber min={1} style={{ width: '100%' }} />
            </Form.Item>
          </Col>
        </Row>
        <Row gutter={16}>
          <Col span={12}>
            <Form.Item
              name={['labor_config', 'hours_per_week']}
              label="Hours per Week"
              initialValue={40}
            >
              <InputNumber min={0} max={168} style={{ width: '100%' }} />
            </Form.Item>
          </Col>
          <Col span={12}>
            <Form.Item
              name={['labor_config', 'weeks_per_year']}
              label="Weeks per Year"
              initialValue={52}
            >
              <InputNumber min={0} max={52} style={{ width: '100%' }} />
            </Form.Item>
          </Col>
        </Row>
      </Card>

      <Divider />

      <Card title="Project Parameters">
        <Row gutter={16}>
          <Col span={8}>
            <Form.Item
              name="project_duration"
              label="Project Duration (years)"
              rules={[{ required: true, message: 'Please enter project duration' }]}
            >
              <InputNumber min={1} style={{ width: '100%' }} />
            </Form.Item>
          </Col>
          <Col span={8}>
            <Form.Item
              name="discount_rate"
              label="Discount Rate"
              rules={[{ required: true, message: 'Please enter discount rate' }]}
            >
              <InputNumber min={0} max={1} step={0.01} style={{ width: '100%' }} />
            </Form.Item>
          </Col>
          <Col span={8}>
            <Form.Item
              name="production_volume"
              label="Production Volume (kg/year)"
              rules={[{ required: true, message: 'Please enter production volume' }]}
            >
              <InputNumber min={0} style={{ width: '100%' }} />
            </Form.Item>
          </Col>
        </Row>
      </Card>

      <Divider />

      <Card title="Cost Factors">
        <Row gutter={16}>
          <Col span={8}>
            <Form.Item
              name="installation_factor"
              label="Installation Factor"
              initialValue={0.2}
            >
              <InputNumber min={0} max={1} step={0.01} style={{ width: '100%' }} />
            </Form.Item>
          </Col>
          <Col span={8}>
            <Form.Item
              name="indirect_costs_factor"
              label="Indirect Costs Factor"
              initialValue={0.15}
            >
              <InputNumber min={0} max={1} step={0.01} style={{ width: '100%' }} />
            </Form.Item>
          </Col>
          <Col span={8}>
            <Form.Item
              name="maintenance_factor"
              label="Maintenance Factor"
              initialValue={0.05}
            >
              <InputNumber min={0} max={1} step={0.01} style={{ width: '100%' }} />
            </Form.Item>
          </Col>
        </Row>
      </Card>
    </div>
  );
};

export default EconomicInputForm;

"use client";

import React from 'react';
import { Form, InputNumber, Row, Col, Card, Divider, Select } from 'antd';
import { FormInstance } from 'antd/lib/form';
import { ALLOCATION_METHODS } from '../../config/constants';

interface EnvironmentalInputFormProps {
  form: FormInstance;
  onSuccess: (response: any) => Promise<void>;
  loading: boolean;
}

const EnvironmentalInputForm: React.FC<EnvironmentalInputFormProps> = ({ form, onSuccess, loading }) => {
  return (
    <div className="environmental-input-form">
      <Card title="Energy Consumption">
        <Row gutter={16}>
          <Col span={8}>
            <Form.Item
              name={['energy_consumption', 'electricity']}
              label="Electricity Consumption (kWh)"
              rules={[{ required: true, message: 'Please enter electricity consumption' }]}
            >
              <InputNumber min={0} style={{ width: '100%' }} />
            </Form.Item>
          </Col>
          <Col span={8}>
            <Form.Item
              name={['energy_consumption', 'cooling']}
              label="Cooling Consumption (kWh)"
              rules={[{ required: true, message: 'Please enter cooling consumption' }]}
            >
              <InputNumber min={0} style={{ width: '100%' }} />
            </Form.Item>
          </Col>
          <Col span={8}>
            <Form.Item
              name="thermal_ratio"
              label="Thermal Energy Ratio"
              initialValue={0.3}
            >
              <InputNumber min={0} max={1} step={0.01} style={{ width: '100%' }} />
            </Form.Item>
          </Col>
        </Row>
      </Card>

      <Divider />

      <Card title="Resource Consumption">
        <Row gutter={16}>
          <Col span={8}>
            <Form.Item
              name="water_consumption"
              label="Water Consumption (kg)"
              rules={[{ required: true, message: 'Please enter water consumption' }]}
            >
              <InputNumber min={0} style={{ width: '100%' }} />
            </Form.Item>
          </Col>
          <Col span={8}>
            <Form.Item
              name="transport_consumption"
              label="Transport Energy (MJ)"
              rules={[{ required: true, message: 'Please enter transport energy' }]}
            >
              <InputNumber min={0} style={{ width: '100%' }} />
            </Form.Item>
          </Col>
          <Col span={8}>
            <Form.Item
              name="equipment_mass"
              label="Equipment Mass (kg)"
              rules={[{ required: true, message: 'Please enter equipment mass' }]}
            >
              <InputNumber min={0} style={{ width: '100%' }} />
            </Form.Item>
          </Col>
        </Row>
      </Card>

      <Divider />

      <Card title="Production Data">
        <Row gutter={16}>
          <Col span={8}>
            <Form.Item
              name={['production_data', 'input_mass']}
              label="Input Mass (kg)"
              rules={[{ required: true, message: 'Please enter input mass' }]}
            >
              <InputNumber min={0} style={{ width: '100%' }} />
            </Form.Item>
          </Col>
          <Col span={8}>
            <Form.Item
              name={['production_data', 'output_mass']}
              label="Output Mass (kg)"
              rules={[{ required: true, message: 'Please enter output mass' }]}
            >
              <InputNumber min={0} style={{ width: '100%' }} />
            </Form.Item>
          </Col>
          <Col span={8}>
            <Form.Item
              name={['production_data', 'production_volume']}
              label="Production Volume (kg/year)"
              rules={[{ required: true, message: 'Please enter production volume' }]}
            >
              <InputNumber min={0} style={{ width: '100%' }} />
            </Form.Item>
          </Col>
        </Row>
      </Card>

      <Divider />

      <Card title="Product Values">
        <Row gutter={16}>
          <Col span={12}>
            <Form.Item
              name={['product_values', 'main_product']}
              label="Main Product Value (USD)"
              rules={[{ required: true, message: 'Please enter main product value' }]}
            >
              <InputNumber min={0} style={{ width: '100%' }} />
            </Form.Item>
          </Col>
          <Col span={12}>
            <Form.Item
              name={['product_values', 'waste_product']}
              label="Waste Product Value (USD)"
              initialValue={0}
            >
              <InputNumber min={0} style={{ width: '100%' }} />
            </Form.Item>
          </Col>
        </Row>
      </Card>

      <Divider />

      <Card title="Impact Allocation">
        <Row gutter={16}>
          <Col span={12}>
            <Form.Item
              name="allocation_method"
              label="Allocation Method"
              initialValue="hybrid"
            >
              <Select options={ALLOCATION_METHODS} />
            </Form.Item>
          </Col>
        </Row>
        <Row gutter={16}>
          <Col span={12}>
            <Form.Item
              name={['hybrid_weights', 'physical']}
              label="Physical Weight"
              initialValue={0.5}
            >
              <InputNumber min={0} max={1} step={0.01} style={{ width: '100%' }} />
            </Form.Item>
          </Col>
          <Col span={12}>
            <Form.Item
              name={['hybrid_weights', 'economic']}
              label="Economic Weight"
              initialValue={0.5}
            >
              <InputNumber min={0} max={1} step={0.01} style={{ width: '100%' }} />
            </Form.Item>
          </Col>
        </Row>
      </Card>
    </div>
  );
};

export default EnvironmentalInputForm;

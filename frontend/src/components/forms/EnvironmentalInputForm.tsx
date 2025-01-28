"use client";

import React from 'react';
import { Form, InputNumber, Row, Col, Card, Button, Tooltip } from 'antd';
import { InfoCircleOutlined } from '@ant-design/icons';

interface EnvironmentalInputFormProps {
  onSubmit: (values: any) => Promise<void>;
  isSubmitting?: boolean;
}

const EnvironmentalInputForm: React.FC<EnvironmentalInputFormProps> = ({
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
      <Card title="Energy Consumption" className="mb-6">
        <Row gutter={16}>
          <Col span={12}>
            <Form.Item
              name="electricity_consumption"
              label={
                <span>
                  Electricity Consumption (kWh)
                  <Tooltip title="Total electricity consumption for the process">
                    <InfoCircleOutlined className="ml-1" />
                  </Tooltip>
                </span>
              }
              rules={[{ required: true, message: 'Please enter electricity consumption' }]}
            >
              <InputNumber min={0} style={{ width: '100%' }} />
            </Form.Item>
          </Col>
          <Col span={12}>
            <Form.Item
              name="thermal_energy"
              label={
                <span>
                  Thermal Energy (kWh)
                  <Tooltip title="Thermal energy required for the process">
                    <InfoCircleOutlined className="ml-1" />
                  </Tooltip>
                </span>
              }
              rules={[{ required: true, message: 'Please enter thermal energy consumption' }]}
            >
              <InputNumber min={0} style={{ width: '100%' }} />
            </Form.Item>
          </Col>
        </Row>
      </Card>

      <Card title="Water Usage" className="mb-6">
        <Row gutter={16}>
          <Col span={12}>
            <Form.Item
              name="water_consumption"
              label={
                <span>
                  Water Consumption (m³)
                  <Tooltip title="Total water consumption in the process">
                    <InfoCircleOutlined className="ml-1" />
                  </Tooltip>
                </span>
              }
              rules={[{ required: true, message: 'Please enter water consumption' }]}
            >
              <InputNumber min={0} style={{ width: '100%' }} />
            </Form.Item>
          </Col>
          <Col span={12}>
            <Form.Item
              name="wastewater_generation"
              label={
                <span>
                  Wastewater Generation (m³)
                  <Tooltip title="Volume of wastewater generated">
                    <InfoCircleOutlined className="ml-1" />
                  </Tooltip>
                </span>
              }
              rules={[
                { required: true, message: 'Please enter wastewater generation' },
                ({ getFieldValue }) => ({
                  validator(_, value) {
                    if (!value || getFieldValue('water_consumption') >= value) {
                      return Promise.resolve();
                    }
                    return Promise.reject(new Error('Wastewater cannot exceed water consumption'));
                  },
                }),
              ]}
            >
              <InputNumber min={0} style={{ width: '100%' }} />
            </Form.Item>
          </Col>
        </Row>
      </Card>

      <Card title="Waste Management" className="mb-6">
        <Row gutter={16}>
          <Col span={12}>
            <Form.Item
              name="solid_waste"
              label={
                <span>
                  Solid Waste Generation (kg)
                  <Tooltip title="Amount of solid waste produced">
                    <InfoCircleOutlined className="ml-1" />
                  </Tooltip>
                </span>
              }
              rules={[{ required: true, message: 'Please enter solid waste generation' }]}
            >
              <InputNumber min={0} style={{ width: '100%' }} />
            </Form.Item>
          </Col>
          <Col span={12}>
            <Form.Item
              name="recyclable_waste"
              label={
                <span>
                  Recyclable Waste (kg)
                  <Tooltip title="Amount of waste that can be recycled">
                    <InfoCircleOutlined className="ml-1" />
                  </Tooltip>
                </span>
              }
              rules={[
                { required: true, message: 'Please enter recyclable waste amount' },
                ({ getFieldValue }) => ({
                  validator(_, value) {
                    if (!value || getFieldValue('solid_waste') >= value) {
                      return Promise.resolve();
                    }
                    return Promise.reject(new Error('Recyclable waste cannot exceed total solid waste'));
                  },
                }),
              ]}
            >
              <InputNumber min={0} style={{ width: '100%' }} />
            </Form.Item>
          </Col>
        </Row>
      </Card>

      <Card title="Transportation" className="mb-6">
        <Row gutter={16}>
          <Col span={12}>
            <Form.Item
              name="transport_distance"
              label={
                <span>
                  Transport Distance (km)
                  <Tooltip title="Total transportation distance for materials">
                    <InfoCircleOutlined className="ml-1" />
                  </Tooltip>
                </span>
              }
              rules={[{ required: true, message: 'Please enter transport distance' }]}
            >
              <InputNumber min={0} style={{ width: '100%' }} />
            </Form.Item>
          </Col>
          <Col span={12}>
            <Form.Item
              name="transport_load"
              label={
                <span>
                  Transport Load (tons)
                  <Tooltip title="Total mass of materials transported">
                    <InfoCircleOutlined className="ml-1" />
                  </Tooltip>
                </span>
              }
              rules={[{ required: true, message: 'Please enter transport load' }]}
            >
              <InputNumber min={0} style={{ width: '100%' }} />
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

export default EnvironmentalInputForm;

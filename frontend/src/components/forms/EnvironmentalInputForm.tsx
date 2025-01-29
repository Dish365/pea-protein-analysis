"use client";

import React from 'react';
import { Form, InputNumber, Row, Col, Card, Button, Tooltip, Space, FormInstance } from 'antd';
import { InfoCircleOutlined } from '@ant-design/icons';
import { formatNumber } from '@/lib/formatters';
import { DEFAULT_PROCESS_ANALYSIS } from '@/config/constants';
import { EnvironmentalParameters } from '@/types/environmental';

interface EnvironmentalInputFormProps {
  form: FormInstance;
  onSubmit: (values: EnvironmentalParameters) => Promise<void>;
  isSubmitting?: boolean;
  initialValues?: Partial<EnvironmentalParameters>;
}

const EnvironmentalInputForm: React.FC<EnvironmentalInputFormProps> = ({
  form,
  onSubmit,
  isSubmitting = false,
  initialValues = DEFAULT_PROCESS_ANALYSIS,
}) => {
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
      <Card title="Energy Consumption" className="mb-6 shadow-sm">
        <Row gutter={16}>
          <Col span={8}>
            <Form.Item
              name="electricity_consumption"
              label={
                <FormLabel 
                  label="Electricity (kWh)" 
                  tooltip="Total electrical energy consumed in the process"
                />
              }
              rules={[{ required: true, type: 'number', min: 0 }]}
            >
              <InputNumber
                min={0}
                step={10}
                formatter={(value) => formatNumber(value as number)}
                parser={(value: string | undefined): number => value ? parseFloat(value.replace(/[^\d.]/g, '')) : 0}
                style={{ width: '100%' }}
                className="text-right"
              />
            </Form.Item>
          </Col>
          <Col span={8}>
            <Form.Item
              name="thermal_energy"
              label={
                <FormLabel 
                  label="Thermal Energy (kWh)" 
                  tooltip="Thermal energy required for heating processes"
                />
              }
              rules={[{ required: true, type: 'number', min: 0 }]}
            >
              <InputNumber
                min={0}
                step={10}
                formatter={(value) => formatNumber(value as number)}
                parser={(value: string | undefined): number => value ? parseFloat(value.replace(/[^\d.]/g, '')) : 0}
                style={{ width: '100%' }}
                className="text-right"
              />
            </Form.Item>
          </Col>
          <Col span={8}>
            <Form.Item
              name="cooling_consumption"
              label={
                <FormLabel 
                  label="Cooling Energy (kWh)" 
                  tooltip="Energy consumed for cooling processes"
                />
              }
              rules={[{ required: true, type: 'number', min: 0 }]}
            >
              <InputNumber
                min={0}
                step={10}
                formatter={(value) => formatNumber(value as number)}
                parser={(value: string | undefined): number => value ? parseFloat(value.replace(/[^\d.]/g, '')) : 0}
                style={{ width: '100%' }}
                className="text-right"
              />
            </Form.Item>
          </Col>
        </Row>
      </Card>

      <Card title="Water Usage" className="mb-6 shadow-sm">
        <Row gutter={16}>
          <Col span={12}>
            <Form.Item
              name="water_consumption"
              label={
                <FormLabel 
                  label="Water Consumption (m³)" 
                  tooltip="Total water used in the process including cleaning and cooling"
                />
              }
              rules={[{ required: true, type: 'number', min: 0 }]}
            >
              <InputNumber
                min={0}
                step={0.1}
                formatter={(value) => formatNumber(value as number)}
                parser={(value: string | undefined): number => value ? parseFloat(value.replace(/[^\d.]/g, '')) : 0}
                style={{ width: '100%' }}
                className="text-right"
              />
            </Form.Item>
          </Col>
          <Col span={12}>
            <Form.Item
              name="wastewater_generation"
              label={
                <FormLabel 
                  label="Wastewater Generation (m³)" 
                  tooltip="Volume of contaminated water requiring treatment"
                />
              }
              rules={[
                { required: true, type: 'number', min: 0 },
                ({ getFieldValue }) => ({
                  validator(_, value) {
                    if (!value || getFieldValue('water_consumption') >= value) {
                      return Promise.resolve();
                    }
                    return Promise.reject('Wastewater cannot exceed water consumption');
                  },
                }),
              ]}
            >
              <InputNumber
                min={0}
                step={0.1}
                formatter={(value) => formatNumber(value as number)}
                parser={(value: string | undefined): number => value ? parseFloat(value.replace(/[^\d.]/g, '')) : 0}
                style={{ width: '100%' }}
                className="text-right"
              />
            </Form.Item>
          </Col>
        </Row>
      </Card>

      <Card title="Waste Management" className="mb-6 shadow-sm">
        <Row gutter={16}>
          <Col span={12}>
            <Form.Item
              name="solid_waste"
              label={
                <FormLabel 
                  label="Solid Waste (kg)" 
                  tooltip="Total solid waste generated during processing"
                />
              }
              rules={[{ required: true, type: 'number', min: 0 }]}
            >
              <InputNumber
                min={0}
                step={1}
                formatter={(value) => formatNumber(value as number)}
                parser={(value: string | undefined): number => value ? parseFloat(value.replace(/[^\d.]/g, '')) : 0}
                style={{ width: '100%' }}
                className="text-right"
              />
            </Form.Item>
          </Col>
          <Col span={12}>
            <Form.Item
              name="recyclable_waste"
              label={
                <FormLabel 
                  label="Recyclable Waste (kg)" 
                  tooltip="Amount of waste suitable for recycling or reuse"
                />
              }
              rules={[
                { required: true, type: 'number', min: 0 },
                ({ getFieldValue }) => ({
                  validator(_, value) {
                    if (!value || getFieldValue('solid_waste') >= value) {
                      return Promise.resolve();
                    }
                    return Promise.reject('Recyclable waste cannot exceed total solid waste');
                  },
                }),
              ]}
            >
              <InputNumber
                min={0}
                step={1}
                formatter={(value) => formatNumber(value as number)}
                parser={(value: string | undefined): number => value ? parseFloat(value.replace(/[^\d.]/g, '')) : 0}
                style={{ width: '100%' }}
                className="text-right"
              />
            </Form.Item>
          </Col>
        </Row>
      </Card>

      <Card title="Transportation" className="mb-6 shadow-sm">
        <Row gutter={16}>
          <Col span={8}>
            <Form.Item
              name="transport_distance"
              label={
                <FormLabel 
                  label="Transport Distance (km)" 
                  tooltip="Total distance for material transportation"
                />
              }
              rules={[{ required: true, type: 'number', min: 0 }]}
            >
              <InputNumber
                min={0}
                step={10}
                formatter={(value) => formatNumber(value as number)}
                parser={(value: string | undefined): number => value ? parseFloat(value.replace(/[^\d.]/g, '')) : 0}
                style={{ width: '100%' }}
                className="text-right"
              />
            </Form.Item>
          </Col>
          <Col span={8}>
            <Form.Item
              name="transport_load"
              label={
                <FormLabel 
                  label="Transport Load (tons)" 
                  tooltip="Total mass of materials being transported"
                />
              }
              rules={[{ required: true, type: 'number', min: 0 }]}
            >
              <InputNumber
                min={0}
                step={0.1}
                formatter={(value) => formatNumber(value as number)}
                parser={(value: string | undefined): number => value ? parseFloat(value.replace(/[^\d.]/g, '')) : 0}
                style={{ width: '100%' }}
                className="text-right"
              />
            </Form.Item>
          </Col>
          <Col span={8}>
            <Form.Item
              name="equipment_mass"
              label={
                <FormLabel 
                  label="Equipment Mass (kg)" 
                  tooltip="Total mass of process equipment"
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
          Complete Analysis Setup
        </Button>
      </div>
    </Form>
  );
};

export default EnvironmentalInputForm;

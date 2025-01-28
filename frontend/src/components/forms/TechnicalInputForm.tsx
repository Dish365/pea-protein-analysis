"use client";

import React from 'react';
import { Form, Select, InputNumber, Row, Col, Card, Button, Tooltip, Space } from 'antd';
import { PROCESS_TYPES, DEFAULT_PROCESS_ANALYSIS } from '../../config/constants';
import { TechnicalParameters } from '@/types/technical';
import { formatNumber } from '@/lib/formatters';
import { InfoCircleOutlined } from '@ant-design/icons';

interface TechnicalInputFormProps {
  onSubmit: (values: TechnicalParameters) => Promise<void>;
  isSubmitting?: boolean;
  initialValues?: Partial<TechnicalParameters>;
}

const TechnicalInputForm: React.FC<TechnicalInputFormProps> = ({
  onSubmit,
  isSubmitting = false,
  initialValues = DEFAULT_PROCESS_ANALYSIS,
}) => {
  const [form] = Form.useForm<TechnicalParameters>();

  // Helper function for form item tooltip
  const FormLabel = ({ label, tooltip }: { label: string; tooltip: string }) => (
    <Space>
      {label}
      <Tooltip title={tooltip}>
        <InfoCircleOutlined style={{ color: '#1890ff' }} />
      </Tooltip>
    </Space>
  );

  const handleSubmit = async (values: TechnicalParameters) => {
    await onSubmit(values);
  };

  return (
    <Form
      form={form}
      layout="vertical"
      onFinish={handleSubmit}
      initialValues={initialValues}
      className="max-w-4xl mx-auto"
    >
      <Card title="Process Configuration" className="mb-6 shadow-sm">
        <Row gutter={16}>
          <Col span={12}>
            <Form.Item
              name="process_type"
              label={
                <FormLabel 
                  label="Process Type" 
                  tooltip="Select the type of process to analyze"
                />
              }
              rules={[{ required: true }]}
            >
              <Select>
                {PROCESS_TYPES.map(({ value, label }) => (
                  <Select.Option key={value} value={value}>
                    {label}
                  </Select.Option>
                ))}
              </Select>
            </Form.Item>
          </Col>
          <Col span={12}>
            <Form.Item
              name="air_flow"
              label={
                <FormLabel 
                  label="Air Flow Rate (m³/h)" 
                  tooltip="Volume of air flowing through the system per hour"
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
              />
            </Form.Item>
          </Col>
        </Row>
      </Card>

      <Card title="Mass & Content Analysis" className="mb-6 shadow-sm">
        <Row gutter={16}>
          <Col span={12}>
            <Form.Item
              name="input_mass"
              label={
                <FormLabel 
                  label="Input Mass (kg)" 
                  tooltip="Total mass of material entering the process"
                />
              }
              rules={[{ required: true, type: 'number', min: 0 }]}
            >
              <InputNumber
                min={0}
                formatter={(value) => formatNumber(value as number)}
                parser={(value: string | undefined): number => value ? parseFloat(value.replace(/[^\d.]/g, '')) : 0}
                style={{ width: '100%' }}
              />
            </Form.Item>
          </Col>
          <Col span={12}>
            <Form.Item
              name="output_mass"
              label={
                <FormLabel 
                  label="Output Mass (kg)" 
                  tooltip="Expected mass of material after processing"
                />
              }
              rules={[
                { required: true, type: 'number', min: 0 },
                ({ getFieldValue }) => ({
                  validator(_, value) {
                    if (!value || getFieldValue('input_mass') >= value) {
                      return Promise.resolve();
                    }
                    return Promise.reject('Output mass cannot exceed input mass');
                  },
                }),
              ]}
            >
              <InputNumber
                min={0}
                formatter={(value) => formatNumber(value as number)}
                parser={(value: string | undefined): number => value ? parseFloat(value.replace(/[^\d.]/g, '')) : 0}
                style={{ width: '100%' }}
              />
            </Form.Item>
          </Col>
        </Row>

        <Row gutter={16} className="mt-4">
          <Col span={12}>
            <Form.Item
              name="initial_protein_content"
              label={
                <FormLabel 
                  label="Initial Protein Content (%)" 
                  tooltip="Protein percentage in input material"
                />
              }
              rules={[{ required: true, type: 'number', min: 0, max: 100 }]}
            >
              <InputNumber
                min={0}
                max={100}
                formatter={(value) => `${value}%`}
                parser={(value: string | undefined): number => value ? parseFloat(value.replace(/[^0-9.]/g, '')) : 0}
                style={{ width: '100%' }}
              />
            </Form.Item>
          </Col>
          <Col span={12}>
            <Form.Item
              name="final_protein_content"
              label={
                <FormLabel 
                  label="Target Protein Content (%)" 
                  tooltip="Expected protein percentage after processing"
                />
              }
              rules={[{ required: true, type: 'number', min: 0, max: 100 }]}
            >
              <InputNumber
                min={0}
                max={100}
                formatter={(value) => `${value}%`}
                parser={(value: string | undefined): number => value ? parseFloat(value.replace(/[^0-9.]/g, '')) : 0}
                style={{ width: '100%' }}
              />
            </Form.Item>
          </Col>
        </Row>
      </Card>

      <Card title="Content Analysis" className="mb-6">
        <Row gutter={16}>
          <Col span={12}>
            <Form.Item
              name="initial_moisture_content"
              label="Initial Moisture Content (%)"
              rules={[
                { required: true, message: 'Please enter initial moisture content' },
                { type: 'number', min: 0, max: 100, message: 'Moisture content must be between 0 and 100%' }
              ]}
              initialValue={DEFAULT_PROCESS_ANALYSIS.initial_moisture_content}
            >
              <InputNumber min={0} max={100} style={{ width: '100%' }} />
            </Form.Item>
          </Col>
          <Col span={12}>
            <Form.Item
              name="final_moisture_content"
              label="Final Moisture Content (%)"
              rules={[
                { required: true, message: 'Please enter final moisture content' },
                { type: 'number', min: 0, max: 100, message: 'Moisture content must be between 0 and 100%' },
                ({ getFieldValue }) => ({
                  validator(_, value) {
                    if (!value || getFieldValue('initial_moisture_content') >= value) {
                      return Promise.resolve();
                    }
                    return Promise.reject(new Error('Final moisture cannot exceed initial moisture'));
                  },
                }),
              ]}
              initialValue={DEFAULT_PROCESS_ANALYSIS.final_moisture_content}
            >
              <InputNumber min={0} max={100} style={{ width: '100%' }} />
            </Form.Item>
          </Col>
        </Row>
      </Card>

      <Card title="Particle Size Distribution" className="mb-6 shadow-sm">
        <Row gutter={16}>
          <Col span={8}>
            <Form.Item
              name="d10_particle_size"
              label={
                <FormLabel 
                  label="D10 Particle Size (μm)" 
                  tooltip="Particle size below which 10% of the sample lies"
                />
              }
              rules={[
                { required: true, type: 'number', min: 0 },
                ({ getFieldValue }) => ({
                  validator(_, value) {
                    const d50 = getFieldValue('d50_particle_size');
                    if (!value || !d50 || value <= d50) {
                      return Promise.resolve();
                    }
                    return Promise.reject('D10 must be smaller than D50');
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
              />
            </Form.Item>
          </Col>
          <Col span={8}>
            <Form.Item
              name="d50_particle_size"
              label={
                <FormLabel 
                  label="D50 Particle Size (μm)" 
                  tooltip="Median particle size (50th percentile)"
                />
              }
              rules={[
                { required: true, type: 'number', min: 0 },
                ({ getFieldValue }) => ({
                  validator(_, value) {
                    const d10 = getFieldValue('d10_particle_size');
                    const d90 = getFieldValue('d90_particle_size');
                    if ((!d10 || value >= d10) && (!d90 || value <= d90)) {
                      return Promise.resolve();
                    }
                    return Promise.reject('D50 must be between D10 and D90');
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
              />
            </Form.Item>
          </Col>
          <Col span={8}>
            <Form.Item
              name="d90_particle_size"
              label={
                <FormLabel 
                  label="D90 Particle Size (μm)" 
                  tooltip="Particle size below which 90% of the sample lies"
                />
              }
              rules={[
                { required: true, type: 'number', min: 0 },
                ({ getFieldValue }) => ({
                  validator(_, value) {
                    const d50 = getFieldValue('d50_particle_size');
                    if (!value || !d50 || value >= d50) {
                      return Promise.resolve();
                    }
                    return Promise.reject('D90 must be larger than D50');
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
              />
            </Form.Item>
          </Col>
        </Row>
      </Card>

      <Card title="Energy Parameters" className="mb-6 shadow-sm">
        <Row gutter={16}>
          <Col span={12}>
            <Form.Item
              name="thermal_ratio"
              label={
                <FormLabel 
                  label="Thermal Energy Ratio" 
                  tooltip="Ratio of thermal to total energy consumption (0-1)"
                />
              }
              rules={[{ required: true, type: 'number', min: 0, max: 1 }]}
            >
              <InputNumber
                min={0}
                max={1}
                step={0.05}
                formatter={(value) => `${(value as number * 100).toFixed(1)}%`}
                parser={(value: string | undefined): number => parseFloat(value!.replace('%', '')) / 100}
                style={{ width: '100%' }}
              />
            </Form.Item>
          </Col>
          <Col span={12}>
            <Form.Item
              name="classifier_speed"
              label={
                <FormLabel 
                  label="Classifier Speed (rpm)" 
                  tooltip="Rotational speed of the classifier wheel"
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
              />
            </Form.Item>
          </Col>
        </Row>

        <Row gutter={16} className="mt-4">
          <Col span={12}>
            <Form.Item
              name="electricity_consumption"
              label={
                <FormLabel 
                  label="Electricity Consumption (kWh)" 
                  tooltip="Expected electrical energy consumption per batch"
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
              />
            </Form.Item>
          </Col>
          <Col span={12}>
            <Form.Item
              name="cooling_consumption"
              label={
                <FormLabel 
                  label="Cooling Energy (kWh)" 
                  tooltip="Expected cooling energy requirement per batch"
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
          Continue to Economic Parameters
        </Button>
      </div>
    </Form>
  );
};

export default TechnicalInputForm;

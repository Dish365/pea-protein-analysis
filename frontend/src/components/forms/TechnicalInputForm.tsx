"use client";

import React from 'react';
import { Form, Input, Select, InputNumber, Row, Col, Card, Divider, Button } from 'antd';
import { FormInstance } from 'antd/lib/form';
import { PROCESS_TYPES, DEFAULT_PROCESS_ANALYSIS } from '../../config/constants';
import { ProcessType } from '@/types/process';

interface TechnicalInputFormProps {
  onSubmit: (values: any) => Promise<void>;
  isSubmitting?: boolean;
}

const TechnicalInputForm: React.FC<TechnicalInputFormProps> = ({
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
      <Card title="Process Configuration" className="mb-6">
        <Row gutter={16}>
          <Col span={12}>
            <Form.Item
              name="process_type"
              label="Process Type"
              rules={[{ required: true, message: 'Please select process type' }]}
            >
              <Select>
                {Object.values(ProcessType).map((type) => (
                  <Select.Option key={type} value={type}>
                    {type}
                  </Select.Option>
                ))}
              </Select>
            </Form.Item>
          </Col>
        </Row>
        <Row gutter={16}>
          <Col span={12}>
            <Form.Item
              name="air_flow"
              label="Air Flow (m³/h)"
              rules={[{ required: true, message: 'Please enter air flow rate' }]}
            >
              <InputNumber min={0} style={{ width: '100%' }} />
            </Form.Item>
          </Col>
          <Col span={12}>
            <Form.Item
              name="classifier_speed"
              label="Classifier Speed (rpm)"
              rules={[{ required: true, message: 'Please enter classifier speed' }]}
            >
              <InputNumber min={0} style={{ width: '100%' }} />
            </Form.Item>
          </Col>
        </Row>
      </Card>

      <Card title="Mass Balance" className="mb-6">
        <Row gutter={16}>
          <Col span={12}>
            <Form.Item
              name="input_mass"
              label="Input Mass (kg)"
              rules={[
                { required: true, message: 'Please enter input mass' },
                { type: 'number', min: 0, message: 'Input mass must be positive' }
              ]}
              initialValue={DEFAULT_PROCESS_ANALYSIS.input_mass}
            >
              <InputNumber min={0} style={{ width: '100%' }} />
            </Form.Item>
          </Col>
          <Col span={12}>
            <Form.Item
              name="output_mass"
              label="Output Mass (kg)"
              rules={[
                { required: true, message: 'Please enter output mass' },
                { type: 'number', min: 0, message: 'Output mass must be positive' },
                ({ getFieldValue }) => ({
                  validator(_, value) {
                    if (!value || getFieldValue('input_mass') >= value) {
                      return Promise.resolve();
                    }
                    return Promise.reject(new Error('Output mass cannot exceed input mass'));
                  },
                }),
              ]}
              initialValue={DEFAULT_PROCESS_ANALYSIS.output_mass}
            >
              <InputNumber min={0} style={{ width: '100%' }} />
            </Form.Item>
          </Col>
        </Row>
      </Card>

      <Card title="Content Analysis" className="mb-6">
        <Row gutter={16}>
          <Col span={12}>
            <Form.Item
              name="initial_protein_content"
              label="Initial Protein Content (%)"
              rules={[
                { required: true, message: 'Please enter initial protein content' },
                { type: 'number', min: 0, max: 100, message: 'Protein content must be between 0 and 100%' }
              ]}
              initialValue={DEFAULT_PROCESS_ANALYSIS.initial_protein_content}
            >
              <InputNumber min={0} max={100} style={{ width: '100%' }} />
            </Form.Item>
          </Col>
          <Col span={12}>
            <Form.Item
              name="final_protein_content"
              label="Final Protein Content (%)"
              rules={[
                { required: true, message: 'Please enter final protein content' },
                { type: 'number', min: 0, max: 100, message: 'Protein content must be between 0 and 100%' }
              ]}
              initialValue={DEFAULT_PROCESS_ANALYSIS.final_protein_content}
            >
              <InputNumber min={0} max={100} style={{ width: '100%' }} />
            </Form.Item>
          </Col>
        </Row>
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

      <Card title="Particle Size Distribution" className="mb-6">
        <Row gutter={16}>
          <Col span={8}>
            <Form.Item
              name="d10_particle_size"
              label="D10 Particle Size (μm)"
              rules={[
                { required: true, message: 'Please enter D10 particle size' },
                { type: 'number', min: 0, message: 'Particle size must be positive' }
              ]}
              initialValue={DEFAULT_PROCESS_ANALYSIS.d10_particle_size}
            >
              <InputNumber min={0} style={{ width: '100%' }} />
            </Form.Item>
          </Col>
          <Col span={8}>
            <Form.Item
              name="d50_particle_size"
              label="D50 Particle Size (μm)"
              rules={[
                { required: true, message: 'Please enter D50 particle size' },
                { type: 'number', min: 0, message: 'Particle size must be positive' },
                ({ getFieldValue }) => ({
                  validator(_, value) {
                    if (!value || value >= getFieldValue('d10_particle_size')) {
                      return Promise.resolve();
                    }
                    return Promise.reject(new Error('D50 must be larger than D10'));
                  },
                }),
              ]}
              initialValue={DEFAULT_PROCESS_ANALYSIS.d50_particle_size}
            >
              <InputNumber min={0} style={{ width: '100%' }} />
            </Form.Item>
          </Col>
          <Col span={8}>
            <Form.Item
              name="d90_particle_size"
              label="D90 Particle Size (μm)"
              rules={[
                { required: true, message: 'Please enter D90 particle size' },
                { type: 'number', min: 0, message: 'Particle size must be positive' },
                ({ getFieldValue }) => ({
                  validator(_, value) {
                    if (!value || value >= getFieldValue('d50_particle_size')) {
                      return Promise.resolve();
                    }
                    return Promise.reject(new Error('D90 must be larger than D50'));
                  },
                }),
              ]}
              initialValue={DEFAULT_PROCESS_ANALYSIS.d90_particle_size}
            >
              <InputNumber min={0} style={{ width: '100%' }} />
            </Form.Item>
          </Col>
        </Row>
      </Card>

      <Card title="Energy Parameters" className="mb-6">
        <Row gutter={16}>
          <Col span={12}>
            <Form.Item
              name="thermal_ratio"
              label="Thermal Energy Ratio"
              rules={[
                { required: true, message: 'Please enter thermal ratio' },
                { type: 'number', min: 0, max: 1, message: 'Ratio must be between 0 and 1' }
              ]}
            >
              <InputNumber min={0} max={1} step={0.01} style={{ width: '100%' }} />
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

export default TechnicalInputForm;

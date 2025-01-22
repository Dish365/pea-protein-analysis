"use client";

import React from 'react';
import { Form, Input, Select, InputNumber, Row, Col, Card, Divider } from 'antd';
import { FormInstance } from 'antd/lib/form';
import { PROCESS_TYPES, DEFAULT_PROCESS_ANALYSIS } from '../../config/constants';

interface TechnicalInputFormProps {
  form: FormInstance;
}

const TechnicalInputForm: React.FC<TechnicalInputFormProps> = ({ form }) => {
  return (
    <div className="technical-input-form">
      <Card title="Process Configuration">
        <Row gutter={16}>
          <Col span={12}>
            <Form.Item
              name="process_type"
              label="Process Type"
              rules={[{ required: true, message: 'Please select process type' }]}
            >
              <Select options={PROCESS_TYPES} />
            </Form.Item>
          </Col>
        </Row>
        <Row gutter={16}>
          <Col span={12}>
            <Form.Item
              name="air_flow"
              label="Air Flow (m³/h)"
              rules={[{ required: true, message: 'Please enter air flow rate' }]}
              initialValue={DEFAULT_PROCESS_ANALYSIS.air_flow}
            >
              <InputNumber min={0} style={{ width: '100%' }} />
            </Form.Item>
          </Col>
          <Col span={12}>
            <Form.Item
              name="classifier_speed"
              label="Classifier Speed (rpm)"
              rules={[{ required: true, message: 'Please enter classifier speed' }]}
              initialValue={DEFAULT_PROCESS_ANALYSIS.classifier_speed}
            >
              <InputNumber min={0} style={{ width: '100%' }} />
            </Form.Item>
          </Col>
        </Row>
      </Card>

      <Divider />

      <Card title="Mass Balance">
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

      <Divider />

      <Card title="Content Analysis">
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

      <Divider />

      <Card title="Particle Size Distribution">
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
    </div>
  );
};

export default TechnicalInputForm;

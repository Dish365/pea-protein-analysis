"use client";

import React from 'react';
import { Row, Col, Spin } from 'antd';
import ProteinRecoveryCard from './ProteinRecoveryCard';
import EfficiencyMetrics from './EfficiencyMetrics';
import ParticleSizeDisplay from './ParticleSizeDisplay';
import { ProcessAnalysis } from '../../../types/process';

interface TechnicalAnalysisProps {
  data?: ProcessAnalysis;
  loading?: boolean;
}

const TechnicalAnalysis: React.FC<TechnicalAnalysisProps> = ({ data, loading = false }) => {
  if (loading || !data) {
    return (
      <div className="loading-container">
        <Spin size="large" tip="Loading technical analysis..." />
      </div>
    );
  }

  return (
    <div className="technical-analysis">
      <Row gutter={[16, 16]}>
        <Col xs={24} lg={12}>
          <ProteinRecoveryCard
            initialProtein={data.initial_protein_content}
            finalProtein={data.final_protein_content}
            inputMass={data.input_mass}
            outputMass={data.output_mass}
          />
        </Col>
        <Col xs={24} lg={12}>
          <EfficiencyMetrics
            processType={data.process_type}
            inputMass={data.input_mass}
            outputMass={data.output_mass}
            airFlow={data.air_flow}
            classifierSpeed={data.classifier_speed}
          />
        </Col>
        <Col xs={24}>
          <ParticleSizeDisplay
            d10={data.d10_particle_size}
            d50={data.d50_particle_size}
            d90={data.d90_particle_size}
          />
        </Col>
      </Row>
    </div>
  );
};

export default TechnicalAnalysis;
"use client";

import React from 'react';
import { Row, Col } from 'antd';
import { TechnicalAnalysisResult } from '@/types/process';
import EfficiencyMetrics from './EfficiencyMetrics';
import ProteinRecoveryCard from './ProteinRecoveryCard';
import ParticleSizeDisplay from './ParticleSizeDisplay';

interface TechnicalAnalysisViewProps {
  data: TechnicalAnalysisResult;
}

export const TechnicalAnalysisView: React.FC<TechnicalAnalysisViewProps> = ({ data }) => {
  return (
    <div className="technical-analysis">
      <Row gutter={[16, 16]}>
        <Col xs={24} lg={12}>
          <ProteinRecoveryCard
            initialMass={data.protein_recovery.initial_mass}
            finalMass={data.protein_recovery.final_mass}
            recoveryRate={data.protein_recovery.recovery_rate}
            concentrationIncrease={data.protein_recovery.concentration_increase}
          />
        </Col>
        <Col xs={24} lg={12}>
          <EfficiencyMetrics
            massEfficiency={data.efficiency.mass}
            processEfficiency={data.efficiency.process}
            throughputRate={data.efficiency.throughput}
            classifierEfficiency={data.efficiency.classifier}
          />
        </Col>
        <Col xs={24}>
          <ParticleSizeDisplay
            d10={data.particle_size.d10}
            d50={data.particle_size.d50}
            d90={data.particle_size.d90}
            span={data.particle_size.span}
          />
        </Col>
      </Row>
    </div>
  );
};

export default TechnicalAnalysisView; 
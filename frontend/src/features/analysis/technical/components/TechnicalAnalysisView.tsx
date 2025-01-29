"use client";

import React from 'react';
import { Row, Col, Alert } from 'antd';
import { TechnicalResults } from '@/types/technical';
import EfficiencyMetrics from './EfficiencyMetrics';
import ProteinRecoveryCard from './ProteinRecoveryCard';
import ParticleSizeDisplay from './ParticleSizeDisplay';

interface TechnicalAnalysisViewProps {
  data: TechnicalResults;
}

export const TechnicalAnalysisView: React.FC<TechnicalAnalysisViewProps> = ({ data }) => {
  // Early return if no data
  if (!data) {
    return <Alert type="warning" message="No technical analysis data available" />;
  }

  // Extract efficiency metrics
  const efficiencyMetrics = {
    massEfficiency: data.protein_recovery.mass,
    processEfficiency: data.process_efficiency,
    separationEfficiency: data.separation_efficiency,
    proteinYield: data.protein_recovery.yield
  };

  // Extract protein recovery metrics
  const proteinRecovery = {
    massRecovery: data.protein_recovery.mass,
    contentRecovery: data.protein_recovery.content,
    yieldRecovery: data.protein_recovery.yield
  };

  // Extract particle size metrics
  const particleSize = data.particle_size_distribution;

  return (
    <div className="technical-analysis space-y-4">
      <Row gutter={[16, 16]}>
        <Col xs={24} lg={12}>
          <ProteinRecoveryCard
            massRecovery={proteinRecovery.massRecovery}
            contentRecovery={proteinRecovery.contentRecovery}
            yieldRecovery={proteinRecovery.yieldRecovery}
          />
        </Col>
        <Col xs={24} lg={12}>
          <EfficiencyMetrics
            massEfficiency={efficiencyMetrics.massEfficiency}
            processEfficiency={efficiencyMetrics.processEfficiency}
            separationEfficiency={efficiencyMetrics.separationEfficiency}
            proteinYield={efficiencyMetrics.proteinYield}
          />
        </Col>
      </Row>
      {particleSize && (
        <Row>
          <Col xs={24}>
            <ParticleSizeDisplay
              d10={particleSize.d10}
              d50={particleSize.d50}
              d90={particleSize.d90}
              span={(particleSize.d90 - particleSize.d10) / particleSize.d50}
            />
          </Col>
        </Row>
      )}
    </div>
  );
};

export default TechnicalAnalysisView; 
"use client";

import React from 'react';
import { Row, Col } from 'antd';
import { EnvironmentalAnalysisResult } from '@/types/environmental';
import EmissionsBreakdown from './EmissionsBreakdown';
import ResourceConsumption from './ResourceConsumption';
import ImpactMetrics from './ImpactMetrics';
import SustainabilityScore from './SustainabilityScore';

interface EnvironmentalAnalysisViewProps {
  data: EnvironmentalAnalysisResult;
}

export const EnvironmentalAnalysisView: React.FC<EnvironmentalAnalysisViewProps> = ({ data }) => {
  return (
    <div className="environmental-analysis">
      <Row gutter={[16, 16]}>
        <Col xs={24} lg={12}>
          <EmissionsBreakdown emissions={data.emissions} />
        </Col>
        <Col xs={24} lg={12}>
          <ResourceConsumption resources={data.resources} />
        </Col>
        <Col xs={24} lg={12}>
          <ImpactMetrics impacts={data.impacts} />
        </Col>
        <Col xs={24} lg={12}>
          <SustainabilityScore metrics={data.metrics} />
        </Col>
      </Row>
    </div>
  );
};

export default EnvironmentalAnalysisView; 
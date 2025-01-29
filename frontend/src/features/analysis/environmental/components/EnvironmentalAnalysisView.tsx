"use client";

import React from 'react';
import { Row, Col, Card, Alert } from 'antd';
import { EnvironmentalAnalysisResult } from '@/types/environmental';
import EmissionsBreakdown from './EmissionsBreakdown';
import ResourceConsumption from './ResourceConsumption';
import ImpactMetrics from './ImpactMetrics';
import SustainabilityScore from './SustainabilityScore';

interface EnvironmentalAnalysisViewProps {
  data: EnvironmentalAnalysisResult;
  processType: string;
}

export const EnvironmentalAnalysisView: React.FC<EnvironmentalAnalysisViewProps> = ({ 
  data, 
  processType 
}) => {
  if (!data) {
    return <Alert type="error" message="No environmental analysis data available" />;
  }

  return (
    <div className="environmental-analysis space-y-4">
      <Row gutter={[16, 16]}>
        <Col xs={24} lg={12}>
          <EmissionsBreakdown 
            impactAssessment={data.impact_assessment}
            processType={processType}
          />
        </Col>
        <Col xs={24} lg={12}>
          <ResourceConsumption 
            consumptionMetrics={data.consumption_metrics}
            processType={processType}
          />
        </Col>
      </Row>
      <Row gutter={[16, 16]}>
        <Col xs={24} lg={12}>
          <ImpactMetrics 
            impacts={data.impact_assessment}
            allocatedImpacts={data.allocated_impacts}
          />
        </Col>
        <Col xs={24} lg={12}>
          <SustainabilityScore 
            impacts={data.impact_assessment}
            processType={processType}
          />
        </Col>
      </Row>
    </div>
  );
};

export default EnvironmentalAnalysisView; 
"use client";

import React from 'react';
import { Row, Col } from 'antd';
import { EconomicAnalysisResult } from '@/types/economic';
import CostBreakdown from './CostBreakdown';
import ProfitabilityMetrics from './ProfitabilityMetrics';
import SensitivityAnalysis from './SensitivityAnalysis';

interface EconomicAnalysisViewProps {
  data: EconomicAnalysisResult;
}

export const EconomicAnalysisView: React.FC<EconomicAnalysisViewProps> = ({ data }) => {
  return (
    <div className="economic-analysis">
      <Row gutter={[16, 16]}>
        <Col xs={24} lg={12}>
          <CostBreakdown
            costs={data.costs}
            totalCost={data.metrics.totalAnnualCost}
            unitCost={data.metrics.unitCost}
          />
        </Col>
        <Col xs={24} lg={12}>
          <ProfitabilityMetrics metrics={data.metrics} />
        </Col>
        <Col xs={24}>
          <SensitivityAnalysis sensitivityData={data.sensitivity} />
        </Col>
      </Row>
    </div>
  );
};

export default EconomicAnalysisView; 
"use client";

import React from 'react';
import { Row, Col, Spin } from 'antd';
import CostBreakdown from './CostBreakdown';
import ProfitabilityMetrics from './ProfitabilityMetrics';
import SensitivityAnalysis from './SensitivityAnalysis';
import { ProcessAnalysis } from '../../../types/process';

interface EconomicAnalysisProps {
  data?: ProcessAnalysis;
  loading?: boolean;
}

const EconomicAnalysis: React.FC<EconomicAnalysisProps> = ({ data, loading = false }) => {
  if (loading || !data) {
    return (
      <div className="loading-container">
        <Spin size="large" tip="Loading economic analysis..." />
      </div>
    );
  }

  // Calculate annual costs
  const annualCosts = {
    equipment: data.equipment_cost * (1 + data.installation_factor) / data.project_duration,
    maintenance: data.maintenance_cost,
    rawMaterial: data.raw_material_cost * data.production_volume,
    utilities: data.utility_cost * data.production_volume,
    labor: data.labor_cost * data.production_volume,
    indirect: data.equipment_cost * data.indirect_costs_factor,
  };

  // Calculate total costs
  const totalAnnualCost = Object.values(annualCosts).reduce((a, b) => a + b, 0);
  const unitCost = totalAnnualCost / data.production_volume;

  return (
    <div className="economic-analysis">
      <Row gutter={[16, 16]}>
        <Col xs={24} lg={12}>
          <CostBreakdown
            costs={annualCosts}
            totalCost={totalAnnualCost}
            productionVolume={data.production_volume}
            unitCost={unitCost}
          />
        </Col>
        <Col xs={24} lg={12}>
          <ProfitabilityMetrics
            totalCost={totalAnnualCost}
            productionVolume={data.production_volume}
            projectDuration={data.project_duration}
            discountRate={data.discount_rate}
            equipmentCost={data.equipment_cost}
            installationFactor={data.installation_factor}
          />
        </Col>
        <Col xs={24}>
          <SensitivityAnalysis
            baseValues={{
              equipmentCost: data.equipment_cost,
              maintenanceCost: data.maintenance_cost,
              rawMaterialCost: data.raw_material_cost,
              utilityCost: data.utility_cost,
              laborCost: data.labor_cost,
              productionVolume: data.production_volume,
            }}
            sensitivityRange={data.sensitivity_range || 0.2}
            steps={data.steps || 10}
          />
        </Col>
      </Row>
    </div>
  );
};

export default EconomicAnalysis;
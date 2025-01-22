"use client";

import React from 'react';
import { Row, Col, Spin } from 'antd';
import ResourceUsage from './ResourceUsage';
import EcoEfficiencyDisplay from './EcoEfficiencyDisplay';
import ImpactMetrics from './ImpactMetrics';
import { ProcessAnalysis } from '../../../types/process';

interface EnvironmentalAnalysisProps {
  data?: ProcessAnalysis;
  loading?: boolean;
}

const EnvironmentalAnalysis: React.FC<EnvironmentalAnalysisProps> = ({ data, loading = false }) => {
  if (loading || !data) {
    return (
      <div className="loading-container">
        <Spin size="large" tip="Loading environmental analysis..." />
      </div>
    );
  }

  // Calculate resource efficiency metrics
  const resourceMetrics = {
    electricity: {
      consumption: data.electricity_consumption,
      perKg: data.electricity_consumption / data.production_volume,
    },
    cooling: {
      consumption: data.cooling_consumption,
      perKg: data.cooling_consumption / data.production_volume,
    },
    water: {
      consumption: data.water_consumption,
      perKg: data.water_consumption / data.production_volume,
    },
    transport: {
      consumption: data.transport_consumption,
      perKg: data.transport_consumption / data.production_volume,
    },
  };

  // Calculate eco-efficiency indicators
  const ecoEfficiency = {
    energyEfficiency: calculateEnergyEfficiency(data),
    waterEfficiency: data.production_volume / data.water_consumption,
    materialEfficiency: data.output_mass / data.input_mass,
    transportEfficiency: data.production_volume / data.transport_consumption,
  };

  return (
    <div className="environmental-analysis">
      <Row gutter={[16, 16]}>
        <Col xs={24} lg={12}>
          <ResourceUsage
            resourceMetrics={resourceMetrics}
            productionVolume={data.production_volume}
            processType={data.process_type}
          />
        </Col>
        <Col xs={24} lg={12}>
          <EcoEfficiencyDisplay
            ecoEfficiency={ecoEfficiency}
            processType={data.process_type}
            productionVolume={data.production_volume}
          />
        </Col>
        <Col xs={24}>
          <ImpactMetrics
            resourceMetrics={resourceMetrics}
            equipmentMass={data.equipment_mass}
            processType={data.process_type}
            allocationMethod={data.allocation_method}
            productionVolume={data.production_volume}
          />
        </Col>
      </Row>
    </div>
  );
};

// Helper function for energy efficiency calculation
function calculateEnergyEfficiency(data: ProcessAnalysis): number {
  const totalEnergy = data.electricity_consumption + data.cooling_consumption;
  const theoreticalEnergy = data.input_mass * data.thermal_ratio; // Simplified theoretical energy requirement
  return (theoreticalEnergy / totalEnergy) * 100;
}

export default EnvironmentalAnalysis;
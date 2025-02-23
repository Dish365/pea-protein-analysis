import React from 'react';
import { ComprehensiveAnalysisResponse } from '@/types/economic';
import { CostBreakdown } from './CostBreakdown';
import { ProfitabilityMetrics } from './ProfitabilityMetrics';
import { SensitivityAnalysis } from './SensitivityAnalysis';

interface EconomicAnalysisViewProps {
  data: ComprehensiveAnalysisResponse;
}

export const EconomicAnalysisView: React.FC<EconomicAnalysisViewProps> = ({ data }) => {
  return (
    <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-700">
      <div className="transition-all duration-300 hover:translate-y-[-2px]">
        <CostBreakdown data={data} />
      </div>
      <div className="transition-all duration-300 hover:translate-y-[-2px]">
        <ProfitabilityMetrics data={data} />
      </div>
      <div className="transition-all duration-300 hover:translate-y-[-2px]">
        <SensitivityAnalysis data={data} />
      </div>
    </div>
  );
};

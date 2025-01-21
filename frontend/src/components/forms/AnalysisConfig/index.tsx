import React from "react";

interface AnalysisConfigProps {
  onSubmit: (config: AnalysisSettings) => void;
  initialValues?: Partial<AnalysisSettings>;
  isLoading?: boolean;
}

interface AnalysisSettings {
  timeRange: number;
  threshold: number;
  includeHistorical: boolean;
  compareWithBenchmark: boolean;
}

const AnalysisConfig: React.FC<AnalysisConfigProps> = () => {
  return (
    <div className="analysis-config-form">
      {/* Analysis configuration form content will go here */}
    </div>
  );
};

export default AnalysisConfig;

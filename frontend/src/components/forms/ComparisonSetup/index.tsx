import React from "react";

interface ComparisonSetupProps {
  onSubmit: (data: ComparisonConfig) => void;
  initialValues?: Partial<ComparisonConfig>;
  isLoading?: boolean;
}

interface ComparisonConfig {
  baselineDate: string;
  comparisonDate: string;
  metrics: string[];
  normalizeData: boolean;
}

const ComparisonSetup: React.FC<ComparisonSetupProps> = ({ onSubmit }) => {
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit({
      baselineDate: "",
      comparisonDate: "",
      metrics: [],
      normalizeData: false,
    });
  };

  return (
    <div className="comparison-setup">
      <form onSubmit={handleSubmit}>{/* Form fields will go here */}</form>
    </div>
  );
};

export default ComparisonSetup;

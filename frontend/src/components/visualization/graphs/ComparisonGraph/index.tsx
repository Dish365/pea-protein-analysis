import React from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";

interface ComparisonGraphProps {
  baselineData: {
    label: string;
    value: number;
  }[];
  comparisonData: {
    label: string;
    value: number;
  }[];
  title?: string;
  height?: number;
  width?: number;
}

const ComparisonGraph: React.FC<ComparisonGraphProps> = ({
  baselineData,
  comparisonData,
  title,
  height = 400,
  width = 600,
}) => {
  const combinedData = baselineData.map((item, index) => ({
    label: item.label,
    baseline: item.value,
    comparison: comparisonData[index]?.value || 0,
  }));

  return (
    <div className="comparison-graph">
      {title && <h3 className="text-lg font-semibold mb-4">{title}</h3>}
      <ResponsiveContainer width={width} height={height}>
        <BarChart data={combinedData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="label" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Bar dataKey="baseline" fill="#8884d8" name="Baseline" />
          <Bar dataKey="comparison" fill="#82ca9d" name="Comparison" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};

export default ComparisonGraph;

import React from "react";

interface ProcessCardProps {
  title: string;
  metric: string;
  value: string;
  trend: string;
}

const ProcessCard: React.FC<ProcessCardProps> = ({
  title,
  metric,
  value,
  trend,
}) => {
  return (
    <div className="rounded-lg shadow-md bg-white p-4">
      <h3 className="text-lg font-bold">{title}</h3>
      <p>
        {metric}: {value}
      </p>
      <p>Trend: {trend}</p>
    </div>
  );
};

export default ProcessCard;

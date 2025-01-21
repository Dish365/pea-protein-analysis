import React from "react";
import { Line } from "@ant-design/plots";

interface DataPoint {
  [key: string]: number | string;
}

interface LineChartProps {
  data: DataPoint[];
  xField: string;
  yField: string;
  seriesField?: string;
}

const LineChart: React.FC<LineChartProps> = ({
  data,
  xField,
  yField,
  seriesField,
}) => {
  const config = {
    data,
    xField,
    yField,
    seriesField,
    smooth: true,
    animation: {
      appear: {
        animation: "path-in",
        duration: 1000,
      },
    },
  };

  return <Line {...config} />;
};

export default LineChart;

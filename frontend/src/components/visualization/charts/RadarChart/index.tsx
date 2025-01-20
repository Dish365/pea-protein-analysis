import React from "react";
import { ResponsiveRadar } from "@nivo/radar";

interface RadarChartProps {
  data: Array<any>; // TODO: Define proper type
  keys: string[];
  indexBy: string;
}

const RadarChart: React.FC<RadarChartProps> = ({ data, keys, indexBy }) => {
  return (
    <div style={{ height: "400px" }}>
      <ResponsiveRadar
        data={data}
        keys={keys}
        indexBy={indexBy}
        margin={{ top: 70, right: 80, bottom: 40, left: 80 }}
        gridShape="circular"
        dotSize={10}
        enableDots={true}
        dotColor={{ theme: "background" }}
        dotBorderWidth={2}
        colors={{ scheme: "nivo" }}
        blendMode="multiply"
        animate={true}
      />
    </div>
  );
};

export default RadarChart;

export interface EconomicData {
  id: string;
  timestamp: string;
  value: number;
  indicator: string;
  region: string;
}

export interface EconomicIndicator {
  name: string;
  code: string;
  description: string;
  unit: string;
}

export interface EconomicTimeSeriesData {
  indicator: EconomicIndicator;
  data: EconomicData[];
}

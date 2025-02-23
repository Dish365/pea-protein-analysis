import {
  Equipment,
  Utility,
  RawMaterial,
  LaborConfig,
  RevenueData,
  EconomicFactors,
  WorkingCapital,
  EconomicFormValues
} from "@/types/economic";

// Define base equipment configuration
export const DEFAULT_EQUIPMENT: Equipment[] = [
    {
        name: "Extraction Reactor",
        base_cost: 1200000.0,
        processing_capacity: 5000,
        efficiency_factor: 0.78,
        installation_complexity: 1.35,
        maintenance_cost: 45000.0,
        energy_consumption: 180
    },
    {
        name: "Centrifugal Separator",
        base_cost: 650000.0,
        processing_capacity: 2000,
        efficiency_factor: 0.85,
        installation_complexity: 1.25,
        maintenance_cost: 28000.0,
        energy_consumption: 110
    }
];

// Define base utility configuration
export const DEFAULT_UTILITIES: Utility[] = [
    {
        name: "Steam",
        consumption: 1500,
        unit_price: 0.028,
        operating_hours: 6000,
        unit: "kg"
    },
    {
        name: "Electricity",
        consumption: 950,
        unit_price: 0.105,
        operating_hours: 8000,
        unit: "kWh"
    }
];

// Define base raw material configuration
export const DEFAULT_RAW_MATERIALS: RawMaterial[] = [
    {
        name: "Pea Flour",
        quantity: 2500000.0,
        unit_price: 0.92,
        protein_content: 0.25,
        unit: "kg"
    },
    {
        name: "NaOH",
        quantity: 15000.0,
        unit_price: 0.35,
        unit: "kg"
    }
];

// Define base labor configuration
export const DEFAULT_LABOR_CONFIG: LaborConfig = {
    hourly_wage: 35.75,
    hours_per_week: 40,
    weeks_per_year: 52,
    num_workers: 15,
    benefits_factor: 0.30
};

// Define base revenue configuration
export const DEFAULT_REVENUE_DATA: RevenueData = {
    product_price: 6.50,
    annual_production: 1500000,
    yield_efficiency: 0.70
};

// Define base economic factors
export const DEFAULT_ECONOMIC_FACTORS: EconomicFactors = {
    installation_factor: 0.35,
    indirect_costs_factor: 0.40,
    maintenance_factor: 0.045,
    project_duration: 10,
    discount_rate: 0.10,
    production_volume: 1500000
};

// Define working capital defaults
export const DEFAULT_WORKING_CAPITAL: WorkingCapital = {
    inventory_months: 3,
    receivables_days: 45,
    payables_days: 30
};

// Define Monte Carlo configuration
export const DEFAULT_MONTE_CARLO = {
    iterations: 10000,
    uncertainty: {
        price: 0.30,
        cost: 0.25
    },
    random_seed: 42
};

// Define sensitivity configuration
export const DEFAULT_SENSITIVITY = {
    variables: ["discount_rate", "production_volume", "operating_costs", "revenue"],
    ranges: {
        "discount_rate": [0.05, 0.15] as [number, number],
        "production_volume": [500.0, 1500.0] as [number, number],
        "operating_costs": [0.8, 1.2] as [number, number],
        "revenue": [0.8, 1.2] as [number, number]
    },
    steps: 15
};

// Define metrics filters
export const DEFAULT_METRICS_FILTERS = {
    include_margins: true,
    include_break_even: true,
    include_cost_structure: true,
    include_efficiency: true,
    include_risk: true
};

// Define indirect factors
export const DEFAULT_INDIRECT_FACTORS = [
    {
        name: "Engineering & Design",
        cost: 275000.0,
        percentage: 0.15
    },
    {
        name: "Construction Management",
        cost: 325000.0,
        percentage: 0.20
    },
    {
        name: "Contingency",
        cost: 275000.0,
        percentage: 0.15,
        reference_base: "direct"
    }
];

export const DEFAULT_ECONOMIC_VALUES: EconomicFormValues = {
    process_type: "baseline",
    economic_factors: DEFAULT_ECONOMIC_FACTORS,
    equipment_list: DEFAULT_EQUIPMENT,
    utilities: DEFAULT_UTILITIES,
    raw_materials: DEFAULT_RAW_MATERIALS,
    labor_config: DEFAULT_LABOR_CONFIG,
    revenue_data: DEFAULT_REVENUE_DATA,
    working_capital: DEFAULT_WORKING_CAPITAL,
    analysis_config: {
        monte_carlo: DEFAULT_MONTE_CARLO,
        sensitivity: DEFAULT_SENSITIVITY,
        metrics_filters: DEFAULT_METRICS_FILTERS
    },
    indirect_factors: DEFAULT_INDIRECT_FACTORS
};







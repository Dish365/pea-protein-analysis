export interface Equipment {
    name: string;
    base_cost: number;
    efficiency_factor: number;
    installation_complexity: number;
    maintenance_cost: number;
    energy_consumption: number;
    processing_capacity: number;
}

export interface Utility {
    name: string;
    consumption: number;
    unit_price: number;
    operating_hours: number;
    unit: string;
}

export interface RawMaterial {
    name: string;
    quantity: number;
    unit_price: number;
    protein_content?: number;
    unit: string;
}

export interface LaborConfig {
    hourly_wage: number;
    hours_per_week: number;
    weeks_per_year: number;
    num_workers: number;
    benefits_factor?: number;
}

export interface EconomicFactors {
    installation_factor: number;
    indirect_costs_factor: number;
    maintenance_factor: number;
    project_duration: number;
    discount_rate: number;
    production_volume: number;
}

export interface RevenueData {
    product_price: number;
    annual_production: number;
    yield_efficiency?: number;
}

export interface WorkingCapital {
    inventory_months: number;
    receivables_days: number;
    payables_days: number;
}

export interface UncertaintyConfig {
    price: number;
    cost: number;
    production?: number;
}

export interface MonteCarloConfig {
    iterations: number;
    uncertainty: UncertaintyConfig;
    random_seed?: number;
}

export interface SensitivityConfig {
    variables: string[];
    ranges: Record<string, [number, number]>;
    steps: number;
}

export interface MetricsFilters {
    include_margins: boolean;
    include_break_even: boolean;
    include_cost_structure: boolean;
    include_efficiency: boolean;
    include_risk: boolean;
}

export interface AnalysisConfig {
    monte_carlo: MonteCarloConfig;
    sensitivity: SensitivityConfig;
    metrics_filters: MetricsFilters;
}

// Input model for the comprehensive analysis
export interface ComprehensiveAnalysisInput {
    process_type: string;
    economic_factors: EconomicFactors;
    equipment_list: Equipment[];
    utilities: Utility[];
    raw_materials: RawMaterial[];
    labor_config: LaborConfig;
    revenue_data: RevenueData;
    analysis_config: AnalysisConfig;
    working_capital: WorkingCapital;
}

// Response models for the comprehensive analysis
export interface WorkingCapitalComponent {
    value: number;
    months?: number;
    days?: number;
}

export interface WorkingCapitalComponents {
    inventory: WorkingCapitalComponent;
    receivables: WorkingCapitalComponent;
    payables: WorkingCapitalComponent;
}

export interface InvestmentEfficiency {
    per_unit: number;
    revenue_to_investment: number;
    opex_to_capex: number;
}

export interface CapexSummary {
    total_capex: number;
    equipment_costs: number;
    installation_costs: number;
    indirect_costs: number;
    working_capital: number;
    total_investment: number;
    base_investment: number;
}

export interface OpexSummary {
    total_opex: number;
    cost_breakdown: {
        fixed_costs: {
            value: number;
            percentage: number;
            breakdown: {
                labor: number;
                maintenance: number;
            };
        };
        variable_costs: {
            value: number;
            percentage: number;
            breakdown: {
                raw_materials: number;
                utilities: number;
            };
        };
    };
}

export interface DetailedCostBreakdown {
    labor: number;
    maintenance: number;
    raw_materials: number;
    utilities: number;
}

export interface CostStructure {
    fixed_costs: {
        value: number;
        percentage: number;
        breakdown: {
            labor: number;
            maintenance: number;
        };
    };
    variable_costs: {
        value: number;
        percentage: number;
        breakdown: {
            raw_materials: number;
            utilities: number;
        };
    };
}

export interface Margins {
    gross_margin: { value: number; percentage?: number };
    operating_margin: { value: number; percentage?: number };
}

export interface BreakEvenAnalysis {
    units: number;
    revenue: number;
}

export interface AnnualPerformance {
    revenue: number;
    operating_costs: number;
    total_costs: number;
}

export interface MonteCarloResults {
    results: {
        mean: number;
        std_dev: number;
        confidence_interval: {
            lower: number;
            upper: number;
        } | [number, number];
    };
}

export interface SensitivityResults {
    [variable: string]: {
        values: number[];
        range: number[];
        base_value: number;
        percent_change: number[];
    };
}

export interface CoreProfitabilityMetrics {
    npv: number;
    roi: number;
    payback: number;
}

// Comprehensive analysis response
export interface ComprehensiveAnalysisResponse {
    process_type: string;
    timestamp: string;
    capex_analysis: {
        capex_summary: {
            total_capex: number;
            equipment_costs: number;
            installation_costs: number;
            indirect_costs: number;
            working_capital: number;
            total_investment: number;
            base_investment: number;
        };
        working_capital_components: {
            inventory: { value: number; months: number };
            receivables: { value: number; days: number };
            payables: { value: number; days: number };
        };
        investment_efficiency: {
            per_unit: number;
            revenue_to_investment: number;
            opex_to_capex: number;
        };
    };
    opex_analysis: {
        opex_summary: {
            total_opex: number;
            cost_breakdown: {
                fixed_costs: { value: number; percentage: number };
                variable_costs: { value: number; percentage: number };
                detailed: {
                    labor: number;
                    maintenance: number;
                    raw_materials: number;
                    utilities: number;
                };
            };
        };
    };
    profitability_analysis: {
        metrics: ProfitabilityMetrics;
        monte_carlo?: MonteCarloResults;
        cash_flows: number[];
    };
    sensitivity_analysis?: Record<string, SensitivityVariable>;
}

export interface EconomicParameters {
    equipment: Equipment[];
    utilities: Utility[];
    raw_materials: RawMaterial[];
    labor_config: LaborConfig;
    revenue_data: RevenueData;
    economic_factors: EconomicFactors;
    process_type: string;
    monte_carlo_iterations?: number;
    uncertainty?: number;
}

export interface ProfitabilityMetric {
    value: number;
    unit: string;
}

export interface ProfitabilityMetrics {
    npv: { value: number };
    roi: { value: number };
    payback: { value: number };
    margins: {
        gross_margin: { value: number };
        operating_margin: { value: number };
    };
    annual_metrics: {
        revenue: number;
        operating_costs: number;
        total_costs: number;
        fixed_costs: number;
        effective_production: number;
    };
    break_even: {
        units: number;
        revenue: number;
        unit_price: number;
        variable_cost_per_unit: number;
    };
    monte_carlo?: {
        results: {
            mean: number;
            std_dev: number;
            confidence_interval: {
                lower: number;
                upper: number;
            } | [number, number];
        };
    };
    cost_structure: {
        fixed_costs: {
            value: number;
            percentage: number;
            breakdown: {
                labor: number;
                maintenance: number;
            };
        };
        variable_costs: {
            value: number;
            percentage: number;
            breakdown: {
                raw_materials: number;
                utilities: number;
            };
        };
    };
    sensitivity_analysis?: {
        [key: string]: {
            values: number[];
            percent_change: number[];
            range: number[];
            base_value: number;
            base_npv: number;
        };
    };
}

export interface SensitivityVariable {
    values: number[];
    range: number[];
    base_value: number;
    percent_change: number[];
}

export interface EconomicResults {
    capex_analysis: {
        summary: CapexSummary;
        equipment_breakdown: Equipment[];
        process_type: string;
    };
    opex_analysis: {
        summary: OpexSummary;
        utilities_breakdown: Utility[];
        raw_materials_breakdown: RawMaterial[];
        labor_breakdown: LaborConfig;
        process_type: string;
    };
    profitability_analysis: {
        metrics: ProfitabilityMetrics;
        monte_carlo?: MonteCarloResults;
        cash_flows: number[];
    };
    sensitivity_analysis: {
        [key: string]: {
            values: number[];
            range: number[];
            base_value: number;
            percent_change: number[];
        };
    };
    metadata: {
        process_type: string;
        timestamp: string;
        data_sources: {
            capex: boolean;
            opex: boolean;
            profitability: boolean;
            sensitivity: boolean;
        };
        analysis_parameters: {
            project_duration: number;
            discount_rate: number;
            monte_carlo_iterations: number;
            uncertainty: number;
        };
    };
}

export interface CostBreakdown {
  equipment_cost: number;
  utilities_cost: number;
  raw_materials_cost: number;
  labor_cost: number;
  maintenance_cost: number;
  indirect_cost: number;
}

export interface EconomicAnalysis {
  parameters: EconomicParameters;
  results?: EconomicResults;
}

export interface IndirectFactor {
    name: string;
    cost: number;
    percentage: number;
    reference_base?: string;
}

// Form Values Type
export interface EconomicFormValues {
    process_type: string;
    economic_factors: EconomicFactors;
    equipment_list: Equipment[];
    utilities: Utility[];
    raw_materials: RawMaterial[];
    labor_config: LaborConfig;
    revenue_data: RevenueData;
    working_capital: WorkingCapital;
    analysis_config: AnalysisConfig;
    indirect_factors: IndirectFactor[];
} 
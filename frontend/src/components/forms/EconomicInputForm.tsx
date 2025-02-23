"use client";

import React from "react";
import { useForm, FormProvider } from "react-hook-form";
import { Button } from "@/components/ui/button";
import { EconomicFormValues } from "@/types/economic";
import { FormSection } from "./shared/FormSection";
import { FormNumberInput } from "./shared/FormNumberInput";
import { TooltipProvider } from "@/components/ui/tooltip";
import { Progress } from "@/components/ui/progress";
import { Card } from "@/components/ui/card";
import { DEFAULT_ECONOMIC_VALUES, DEFAULT_INDIRECT_FACTORS, DEFAULT_SENSITIVITY } from "./index";
import { Alert, AlertTitle, AlertDescription } from "@/components/ui/alert";
import { get } from 'lodash';
import { Separator } from "@/components/ui/separator";

interface EconomicInputFormProps {
  onSubmit: (values: EconomicFormValues) => void;
  isSubmitting?: boolean;
  initialData?: Partial<EconomicFormValues>;
}

export default function EconomicInputForm({
  onSubmit,
  isSubmitting = false,
  initialData
}: EconomicInputFormProps) {
  const form = useForm<EconomicFormValues>({
    defaultValues: {
      ...structuredClone(DEFAULT_ECONOMIC_VALUES),
      ...initialData
    },
    mode: "onChange"
  });

  const getRequiredFields = () => [
    // Equipment fields - Extraction Reactor
    'equipment_list.0.base_cost',
    'equipment_list.0.processing_capacity',
    'equipment_list.0.efficiency_factor',
    'equipment_list.0.installation_complexity',
    'equipment_list.0.maintenance_cost',
    'equipment_list.0.energy_consumption',
    
    // Equipment fields - Centrifugal Separator
    'equipment_list.1.base_cost',
    'equipment_list.1.processing_capacity',
    'equipment_list.1.efficiency_factor',
    'equipment_list.1.installation_complexity',
    'equipment_list.1.maintenance_cost',
    'equipment_list.1.energy_consumption',
    
    // Utilities fields - Steam
    'utilities.0.consumption',
    'utilities.0.unit_price',
    'utilities.0.operating_hours',
    'utilities.0.unit',
    
    // Utilities fields - Electricity
    'utilities.1.consumption',
    'utilities.1.unit_price',
    'utilities.1.operating_hours',
    'utilities.1.unit',
    
    // Raw materials fields - Pea Flour
    'raw_materials.0.quantity',
    'raw_materials.0.unit_price',
    'raw_materials.0.protein_content',
    'raw_materials.0.unit',
    
    // Raw materials fields - NaOH
    'raw_materials.1.quantity',
    'raw_materials.1.unit_price',
    'raw_materials.1.unit',
    
    // Labor config fields
    'labor_config.hourly_wage',
    'labor_config.hours_per_week',
    'labor_config.weeks_per_year',
    'labor_config.num_workers',
    'labor_config.benefits_factor',
    
    // Revenue data fields
    'revenue_data.product_price',
    'revenue_data.annual_production',
    'revenue_data.yield_efficiency',
    
    // Economic factors fields
    'economic_factors.installation_factor',
    'economic_factors.indirect_costs_factor',
    'economic_factors.maintenance_factor',
    'economic_factors.project_duration',
    'economic_factors.discount_rate',
    'economic_factors.production_volume',
    
    // Working capital fields
    'working_capital.inventory_months',
    'working_capital.receivables_days',
    'working_capital.payables_days',

    // Analysis config fields
    'analysis_config.monte_carlo.iterations',
    'analysis_config.monte_carlo.uncertainty.price',
    'analysis_config.monte_carlo.uncertainty.cost',
    'analysis_config.monte_carlo.random_seed',

    // Indirect factors
    'indirect_factors.0.cost',
    'indirect_factors.0.percentage',
    'indirect_factors.1.cost',
    'indirect_factors.1.percentage',
    'indirect_factors.2.cost',
    'indirect_factors.2.percentage'
  ];

  const calculateProgress = () => {
    const fields = getRequiredFields();
    const values = form.getValues();
    const filledFields = fields.filter(field => {
      const value = get(values, field);
      const error = get(form.formState.errors, field);
      return value !== undefined && value !== null && !error;
    });
    return (filledFields.length / fields.length) * 100;
  };

  const progress = calculateProgress();

  const handleFormSubmit = async (data: EconomicFormValues) => {
    // Equipment validation
    for (let i = 0; i < 2; i++) {
      const equipment = data.equipment_list?.[i];
      if (!equipment) {
        form.setError(`equipment_list.${i}`, {
          type: 'manual',
          message: 'Equipment configuration is required'
        });
        return;
      }

      if (!equipment.base_cost || equipment.base_cost <= 0) {
        form.setError(`equipment_list.${i}.base_cost`, {
          type: 'manual',
          message: `${equipment.name} base cost must be positive`
        });
        return;
      }
      
      if (!equipment.efficiency_factor || 
          equipment.efficiency_factor <= 0 || 
          equipment.efficiency_factor > 1) {
        form.setError(`equipment_list.${i}.efficiency_factor`, {
          type: 'manual',
          message: `${equipment.name} efficiency factor must be between 0 and 1`
        });
        return;
      }
    }

    // Utilities validation
    for (let i = 0; i < 2; i++) {
      const utility = data.utilities?.[i];
      if (!utility) {
        form.setError(`utilities.${i}`, {
          type: 'manual',
          message: 'Utility configuration is required'
        });
        return;
      }

      if (!utility.consumption || utility.consumption <= 0) {
        form.setError(`utilities.${i}.consumption`, {
          type: 'manual',
          message: `${utility.name} consumption must be positive`
        });
        return;
      }
      
      if (!utility.operating_hours || 
          utility.operating_hours <= 0 || 
          utility.operating_hours > 8760) {
        form.setError(`utilities.${i}.operating_hours`, {
          type: 'manual',
          message: `${utility.name} operating hours must be between 0 and 8760`
        });
        return;
      }
    }

    // Raw materials validation
    for (let i = 0; i < 2; i++) {
      const material = data.raw_materials?.[i];
      if (!material) {
        form.setError(`raw_materials.${i}`, {
          type: 'manual',
          message: 'Raw material configuration is required'
        });
        return;
      }

      if (!material.quantity || material.quantity <= 0) {
        form.setError(`raw_materials.${i}.quantity`, {
          type: 'manual',
          message: `${material.name} quantity must be positive`
        });
        return;
      }
      
      if (i === 0 && (!material.protein_content || 
          material.protein_content <= 0 || 
          material.protein_content > 1)) {
        form.setError(`raw_materials.${i}.protein_content`, {
          type: 'manual',
          message: 'Pea flour protein content must be between 0 and 1'
        });
        return;
      }
    }

    // Labor config validation
    if (!data.labor_config?.hourly_wage || data.labor_config.hourly_wage <= 0) {
      form.setError('labor_config.hourly_wage', {
        type: 'manual',
        message: 'Hourly wage must be positive'
      });
      return;
    }

    // Revenue data validation
    if (!data.revenue_data?.product_price || data.revenue_data.product_price <= 0) {
      form.setError('revenue_data.product_price', {
        type: 'manual',
        message: 'Product price must be positive'
      });
      return;
    }

    if (!data.revenue_data?.yield_efficiency || 
        data.revenue_data.yield_efficiency <= 0 || 
        data.revenue_data.yield_efficiency > 1) {
      form.setError('revenue_data.yield_efficiency', {
        type: 'manual',
        message: 'Yield efficiency must be between 0 and 1'
      });
      return;
    }

    // Economic factors validation
    if (!data.economic_factors?.installation_factor || 
        data.economic_factors.installation_factor <= 0 || 
        data.economic_factors.installation_factor > 1) {
      form.setError('economic_factors.installation_factor', {
        type: 'manual',
        message: 'Installation factor must be between 0 and 1'
      });
      return;
    }

    // Working capital validation
    if (!data.working_capital?.inventory_months || data.working_capital.inventory_months < 0) {
      form.setError('working_capital.inventory_months', {
        type: 'manual',
        message: 'Inventory months must be non-negative'
      });
      return;
    }

    // Analysis config validation
    if (!data.analysis_config?.monte_carlo?.iterations || 
        data.analysis_config.monte_carlo.iterations < 100 || 
        data.analysis_config.monte_carlo.iterations > 10000) {
      form.setError('analysis_config.monte_carlo.iterations', {
        type: 'manual',
        message: 'Monte Carlo iterations must be between 100 and 10000'
      });
      return;
    }

    // Ensure process type is set
    if (!data.process_type) {
      data.process_type = "baseline";
    }

    // Add required fields and ensure correct structure
    const formData: EconomicFormValues = {
      ...data,
      process_type: "baseline",
      utilities: data.utilities?.map(utility => ({
        ...utility,
        unit: utility.name === "Steam" ? "kg" : "kWh"
      })) ?? [],
      raw_materials: data.raw_materials?.map(material => ({
        ...material,
        unit: "kg"
      })) ?? [],
      analysis_config: {
        ...data.analysis_config,
        sensitivity: {
          variables: ["discount_rate", "production_volume", "operating_costs", "revenue"],
          ranges: {
            discount_rate: [0.05, 0.15],
            production_volume: [
              data.revenue_data.annual_production * 0.5,
              data.revenue_data.annual_production * 1.5
            ],
            operating_costs: [0.8, 1.2],
            revenue: [0.8, 1.2]
          },
          steps: 15
        },
        metrics_filters: {
          include_margins: true,
          include_break_even: true,
          include_cost_structure: true,
          include_efficiency: true,
          include_risk: true
        }
      }
    };

    onSubmit(formData);
  };

  return (
    <TooltipProvider>
      <FormProvider {...form}>
        <div className="space-y-6 max-w-4xl mx-auto">
          <div className="space-y-2 mb-8">
            <div className="flex justify-between items-center">
              <h2 className="text-lg font-semibold">Economic Analysis Parameters</h2>
              <span className="text-sm text-muted-foreground">
                {Math.round(progress)}% Complete
              </span>
            </div>
            <Progress value={progress} className="h-2" />
          </div>

          {form.formState.errors.root?.serverError && (
            <Alert variant="destructive" className="mb-6">
              <AlertTitle>Economic Analysis Error</AlertTitle>
              <div className="max-h-[200px] overflow-y-auto">
                <AlertDescription className="whitespace-pre-line">
                  {form.formState.errors.root.serverError.message}
                </AlertDescription>
              </div>
            </Alert>
          )}

          <form id="economic-form" onSubmit={form.handleSubmit(handleFormSubmit)} className="space-y-8">
            <div className="grid gap-6">
              <Card className="p-6">
                <FormSection 
                  title="Capital Expenditure (CAPEX)" 
                  tooltip="Equipment and installation costs"
                >
                  {/* Extraction Reactor */}
                  <div>
                    <h3 className="text-lg font-semibold mb-4">Extraction Reactor</h3>
                    <div className="grid gap-4 sm:grid-cols-2">
                      <FormNumberInput
                        name="equipment_list.0.base_cost"
                        label="Base Cost"
                        unit="$"
                        min={0}
                        required
                        tooltip="Initial purchase cost of equipment"
                      />
                      <FormNumberInput
                        name="equipment_list.0.efficiency_factor"
                        label="Efficiency Factor"
                        unit="ratio"
                        min={0}
                        max={1}
                        step={0.01}
                        required
                        tooltip="Equipment efficiency factor (0-1)"
                      />
                      <FormNumberInput
                        name="equipment_list.0.installation_complexity"
                        label="Installation Complexity"
                        unit="factor"
                        min={0}
                        max={2}
                        step={0.01}
                        required
                        tooltip="Installation complexity factor (typically 1.2-1.5)"
                      />
                      <FormNumberInput
                        name="equipment_list.0.processing_capacity"
                        label="Processing Capacity"
                        unit="kg/h"
                        min={0}
                        step={100}
                        required
                        tooltip="Equipment processing capacity in kg/h"
                      />
                      <FormNumberInput
                        name="equipment_list.0.maintenance_cost"
                        label="Maintenance Cost"
                        unit="$/year"
                        min={0}
                        required
                        tooltip="Annual maintenance cost"
                      />
                      <FormNumberInput
                        name="equipment_list.0.energy_consumption"
                        label="Energy Consumption"
                        unit="kW"
                        min={0}
                        required
                        tooltip="Equipment energy consumption"
                      />
                    </div>
                  </div>

                  <Separator className="my-6" />

                  {/* Centrifugal Separator */}
                  <div>
                    <h3 className="text-lg font-semibold mb-4">Centrifugal Separator</h3>
                    <div className="grid gap-4 sm:grid-cols-2">
                      <FormNumberInput
                        name="equipment_list.1.base_cost"
                        label="Base Cost"
                        unit="$"
                        min={0}
                        required
                        tooltip="Initial purchase cost of equipment"
                      />
                      <FormNumberInput
                        name="equipment_list.1.efficiency_factor"
                        label="Efficiency Factor"
                        unit="ratio"
                        min={0}
                        max={1}
                        step={0.01}
                        required
                        tooltip="Equipment efficiency factor (0-1)"
                      />
                      <FormNumberInput
                        name="equipment_list.1.installation_complexity"
                        label="Installation Complexity"
                        unit="factor"
                        min={0}
                        required
                        tooltip="Multiplier for installation costs"
                      />
                      <FormNumberInput
                        name="equipment_list.1.processing_capacity"
                        label="Processing Capacity"
                        unit="units"
                        min={0}
                        required
                        tooltip="Equipment processing capacity"
                      />
                      <FormNumberInput
                        name="equipment_list.1.maintenance_cost"
                        label="Maintenance Cost"
                        unit="$/year"
                        min={0}
                        required
                        tooltip="Annual maintenance cost"
                      />
                      <FormNumberInput
                        name="equipment_list.1.energy_consumption"
                        label="Energy Consumption"
                        unit="kW"
                        min={0}
                        required
                        tooltip="Equipment energy consumption"
                      />
                    </div>
                  </div>
                </FormSection>
              </Card>

              <Card className="p-6">
                <FormSection 
                  title="Operational Expenditure (OPEX)" 
                  tooltip="Recurring operational costs"
                >
                  {/* Steam Utility */}
                  <div>
                    <h3 className="text-lg font-semibold mb-4">Steam</h3>
                    <div className="grid gap-4 sm:grid-cols-2">
                      <FormNumberInput
                        name="utilities.0.consumption"
                        label="Consumption"
                        unit="kg/h"
                        min={0}
                        required
                        tooltip="Steam consumption rate"
                      />
                      <FormNumberInput
                        name="utilities.0.unit_price"
                        label="Unit Price"
                        unit="$/kg"
                        min={0}
                        step={0.001}
                        required
                        tooltip="Cost per unit of steam"
                      />
                      <FormNumberInput
                        name="utilities.0.operating_hours"
                        label="Operating Hours"
                        unit="h/year"
                        min={0}
                        max={8760}
                        required
                        tooltip="Annual operating hours"
                      />
                    </div>
                  </div>

                  <Separator className="my-6" />

                  {/* Electricity Utility */}
                  <div>
                    <h3 className="text-lg font-semibold mb-4">Electricity</h3>
                    <div className="grid gap-4 sm:grid-cols-2">
                      <FormNumberInput
                        name="utilities.1.consumption"
                        label="Consumption"
                        unit="kWh"
                        min={0}
                        required
                        tooltip="Electricity consumption rate"
                      />
                      <FormNumberInput
                        name="utilities.1.unit_price"
                        label="Unit Price"
                        unit="$/kWh"
                        min={0}
                        step={0.001}
                        required
                        tooltip="Cost per unit of electricity"
                      />
                      <FormNumberInput
                        name="utilities.1.operating_hours"
                        label="Operating Hours"
                        unit="h/year"
                        min={0}
                        max={8760}
                        required
                        tooltip="Annual operating hours"
                      />
                    </div>
                  </div>

                  <Separator className="my-6" />

                  {/* Raw Materials */}
                  <div>
                    <h3 className="text-lg font-semibold mb-4">Raw Materials</h3>
                    
                    {/* Pea Flour */}
                    <div className="mb-6">
                      <h4 className="text-md font-medium mb-2">Pea Flour</h4>
                      <div className="grid gap-4 sm:grid-cols-2">
                        <FormNumberInput
                          name="raw_materials.0.quantity"
                          label="Quantity"
                          unit="kg/year"
                          min={0}
                          required
                          tooltip="Annual pea flour consumption"
                        />
                        <FormNumberInput
                          name="raw_materials.0.unit_price"
                          label="Unit Price"
                          unit="$/kg"
                          min={0}
                          step={0.001}
                          required
                          tooltip="Cost per unit of pea flour"
                        />
                        <FormNumberInput
                          name="raw_materials.0.protein_content"
                          label="Protein Content"
                          unit="ratio"
                          min={0}
                          max={1}
                          step={0.01}
                          required
                          tooltip="Protein content ratio"
                        />
                      </div>
                    </div>

                    {/* NaOH */}
                    <div>
                      <h4 className="text-md font-medium mb-2">NaOH</h4>
                      <div className="grid gap-4 sm:grid-cols-2">
                        <FormNumberInput
                          name="raw_materials.1.quantity"
                          label="Quantity"
                          unit="kg/year"
                          min={0}
                          required
                          tooltip="Annual NaOH consumption"
                        />
                        <FormNumberInput
                          name="raw_materials.1.unit_price"
                          label="Unit Price"
                          unit="$/kg"
                          min={0}
                          step={0.001}
                          required
                          tooltip="Cost per unit of NaOH"
                        />
                      </div>
                    </div>
                  </div>
                </FormSection>
              </Card>

              <Card className="p-6">
                <FormSection 
                  title="Labor Costs" 
                  tooltip="Workforce expenses"
                >
                  <div className="grid gap-4 sm:grid-cols-2">
                    <FormNumberInput
                      name="labor_config.hourly_wage"
                      label="Hourly Wage"
                      unit="$/h"
                      min={0}
                      step={0.01}
                      required
                      tooltip="Average hourly wage per worker"
                    />
                    <FormNumberInput
                      name="labor_config.num_workers"
                      label="Workforce Size"
                      unit="workers"
                      min={1}
                      step={1}
                      required
                      tooltip="Number of workers"
                    />
                    <FormNumberInput
                      name="labor_config.hours_per_week"
                      label="Weekly Hours"
                      unit="h/week"
                      min={0}
                      max={168}
                      required
                      tooltip="Working hours per week"
                    />
                    <FormNumberInput
                      name="labor_config.weeks_per_year"
                      label="Operating Weeks"
                      unit="weeks/year"
                      min={0}
                      max={52}
                      required
                      tooltip="Operational weeks per year"
                    />
                    <FormNumberInput
                      name="labor_config.benefits_factor"
                      label="Benefits Factor"
                      unit="ratio"
                      min={0}
                      max={1}
                      step={0.01}
                      required
                      tooltip="Employee benefits as ratio of wage (e.g. 0.30 for 30%)"
                    />
                  </div>
                </FormSection>
              </Card>

              <Card className="p-6">
                <FormSection 
                  title="Revenue & Production" 
                  tooltip="Sales and production metrics"
                >
                  <div className="grid gap-4 sm:grid-cols-2">
                    <FormNumberInput
                      name="revenue_data.product_price"
                      label="Product Price"
                      unit="$/kg"
                      min={0}
                      step={0.01}
                      required
                      tooltip="Price per unit of product"
                    />
                    <FormNumberInput
                      name="revenue_data.annual_production"
                      label="Annual Production"
                      unit="kg/year"
                      min={0}
                      required
                      tooltip="Annual production volume"
                    />
                    <FormNumberInput
                      name="revenue_data.yield_efficiency"
                      label="Yield Efficiency"
                      unit="ratio"
                      min={0}
                      max={1}
                      step={0.01}
                      required
                      tooltip="Production yield efficiency"
                    />
                  </div>
                </FormSection>
              </Card>

              <Card className="p-6">
                <FormSection 
                  title="Economic Factors" 
                  tooltip="Project financial parameters"
                >
                  <div className="grid gap-4 sm:grid-cols-2">
                    <FormNumberInput
                      name="economic_factors.installation_factor"
                      label="Installation Factor"
                      unit="ratio"
                      min={0}
                      max={1}
                      step={0.01}
                      required
                      tooltip="Installation cost as ratio of equipment cost"
                    />
                    <FormNumberInput
                      name="economic_factors.indirect_costs_factor"
                      label="Indirect Costs Factor"
                      unit="ratio"
                      min={0}
                      max={1}
                      step={0.01}
                      required
                      tooltip="Indirect costs as ratio of direct costs"
                    />
                    <FormNumberInput
                      name="economic_factors.maintenance_factor"
                      label="Maintenance Factor"
                      unit="ratio"
                      min={0}
                      max={1}
                      step={0.001}
                      required
                      tooltip="Annual maintenance cost as ratio (e.g. 0.045 for 4.5%)"
                    />
                    <FormNumberInput
                      name="economic_factors.project_duration"
                      label="Project Duration"
                      unit="years"
                      min={1}
                      max={50}
                      step={1}
                      required
                      tooltip="Project lifetime"
                    />
                    <FormNumberInput
                      name="economic_factors.discount_rate"
                      label="Discount Rate"
                      unit="ratio"
                      min={0}
                      max={1}
                      step={0.01}
                      required
                      tooltip="Annual discount rate"
                    />
                    <FormNumberInput
                      name="economic_factors.production_volume"
                      label="Production Volume"
                      unit="kg/year"
                      min={0}
                      required
                      tooltip="Annual production volume"
                    />
                  </div>
                </FormSection>
              </Card>

              <Card className="p-6">
                <FormSection 
                  title="Working Capital" 
                  tooltip="Working capital requirements"
                >
                  <div className="grid gap-4 sm:grid-cols-2">
                    <FormNumberInput
                      name="working_capital.inventory_months"
                      label="Inventory Period"
                      unit="months"
                      min={0}
                      required
                      tooltip="Number of months of inventory to maintain"
                    />
                    <FormNumberInput
                      name="working_capital.receivables_days"
                      label="Accounts Receivable"
                      unit="days"
                      min={0}
                      required
                      tooltip="Average collection period"
                    />
                    <FormNumberInput
                      name="working_capital.payables_days"
                      label="Accounts Payable"
                      unit="days"
                      min={0}
                      required
                      tooltip="Average payment period"
                    />
                  </div>
                </FormSection>
              </Card>

              <Card className="p-6">
                <FormSection 
                  title="Analysis Configuration" 
                  tooltip="Monte Carlo and sensitivity analysis parameters"
                >
                  <div className="grid gap-4 sm:grid-cols-2">
                    <FormNumberInput
                      name="analysis_config.monte_carlo.iterations"
                      label="Monte Carlo Iterations"
                      unit="iterations"
                      min={100}
                      max={10000}
                      step={100}
                      required
                      tooltip="Number of Monte Carlo iterations (100-10000)"
                    />
                    <FormNumberInput
                      name="analysis_config.monte_carlo.uncertainty.price"
                      label="Price Uncertainty"
                      unit="ratio"
                      min={0}
                      max={1}
                      step={0.01}
                      required
                      tooltip="Price uncertainty factor (0-1)"
                    />
                    <FormNumberInput
                      name="analysis_config.monte_carlo.uncertainty.cost"
                      label="Cost Uncertainty"
                      unit="ratio"
                      min={0}
                      max={1}
                      step={0.01}
                      required
                      tooltip="Cost uncertainty factor (0-1)"
                    />
                    <FormNumberInput
                      name="analysis_config.monte_carlo.random_seed"
                      label="Random Seed"
                      unit="number"
                      min={1}
                      step={1}
                      required
                      tooltip="Random seed for reproducible results"
                    />
                  </div>
                </FormSection>
              </Card>

              <Card className="p-6">
                <FormSection 
                  title="Indirect Costs" 
                  tooltip="Additional indirect costs"
                >
                  <div className="grid gap-4">
                    {DEFAULT_INDIRECT_FACTORS.map((factor, index) => (
                      <div key={factor.name}>
                        <h4 className="text-md font-medium mb-2">{factor.name}</h4>
                        <div className="grid gap-4 sm:grid-cols-2">
                          <FormNumberInput
                            name={`indirect_factors.${index}.cost`}
                            label="Cost"
                            unit="$"
                            min={0}
                            required
                            tooltip={`${factor.name} cost`}
                          />
                          <FormNumberInput
                            name={`indirect_factors.${index}.percentage`}
                            label="Percentage"
                            unit="ratio"
                            min={0}
                            max={1}
                            step={0.01}
                            required
                            tooltip={`${factor.name} percentage as ratio (0-1)`}
                          />
                        </div>
                        {index < DEFAULT_INDIRECT_FACTORS.length - 1 && (
                          <Separator className="my-4" />
                        )}
                      </div>
                    ))}
                  </div>
                </FormSection>
              </Card>
            </div>

            <div className="flex justify-end space-x-4">
              <Button
                type="submit"
                disabled={isSubmitting}
              >
                {isSubmitting ? "Processing..." : "Calculate Economic Analysis"}
              </Button>
            </div>
          </form>
        </div>
      </FormProvider>
    </TooltipProvider>
  );
}
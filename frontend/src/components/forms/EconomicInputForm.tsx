"use client";

import React from "react";
import { useForm, FormProvider } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import * as z from "zod";
import { Button } from "@/components/ui/button";
import { EconomicParameters } from "@/types/economic";
import { ProcessTypeValues, economicValidationSchema, EconomicValidationData } from "@/types/process";
import { FormSection } from "./shared/FormSection";
import { FormNumberInput } from "./shared/FormNumberInput";
import { FormSelect } from "./shared/FormSelect";
import { TooltipProvider } from "@/components/ui/tooltip";
import { Progress } from "@/components/ui/progress";
import { ArrowRight, Loader2 } from "lucide-react";
import { Card } from "@/components/ui/card";
import { DEFAULT_ECONOMIC_VALUES } from './index';

type EconomicFormValues = EconomicValidationData;

interface EconomicInputFormProps {
  onSubmit: (values: EconomicParameters) => void;
  isSubmitting?: boolean;
  initialData?: EconomicParameters;
}

export default function EconomicInputForm({
  onSubmit,
  isSubmitting = false,
  initialData
}: EconomicInputFormProps) {
  const form = useForm<EconomicFormValues>({
    resolver: zodResolver(economicValidationSchema),
    defaultValues: initialData || DEFAULT_ECONOMIC_VALUES,
    mode: "onChange"
  });

  const getRequiredFields = () => [
    'production_volume', 'operating_hours', 'equipment_cost',
    'utility_cost', 'raw_material_cost', 'labor_cost',
    'maintenance_factor', 'indirect_costs_factor', 'installation_factor',
    'project_duration', 'discount_rate', 'revenue_per_year'
  ];

  const calculateProgress = () => {
    const fields = getRequiredFields();
    const values = form.getValues();
    const filledFields = fields.filter(field => {
      const value = values[field as keyof EconomicFormValues];
      return value !== undefined && value !== null && !form.formState.errors[field as keyof EconomicFormValues];
    });
    return (filledFields.length / fields.length) * 100;
  };

  const progress = calculateProgress();

  const handleFormSubmit = async (data: EconomicFormValues) => {
    // Production parameters
    if (!data.production_volume || data.production_volume <= 0) {
      form.setError('production_volume', {
        type: 'manual',
        message: 'Production volume must be positive'
      });
      return;
    }
    if (!data.operating_hours || data.operating_hours <= 0 || data.operating_hours > 8760) {
      form.setError('operating_hours', {
        type: 'manual',
        message: 'Operating hours must be between 0 and 8760'
      });
      return;
    }

    // Capital costs
    if (!data.equipment_cost || data.equipment_cost <= 0) {
      form.setError('equipment_cost', {
        type: 'manual',
        message: 'Equipment cost must be positive'
      });
      return;
    }
    if (!data.installation_factor || data.installation_factor <= 0 || data.installation_factor > 1) {
      form.setError('installation_factor', {
        type: 'manual',
        message: 'Installation factor must be between 0 and 1'
      });
      return;
    }
    if (!data.indirect_costs_factor || data.indirect_costs_factor <= 0 || data.indirect_costs_factor > 1) {
      form.setError('indirect_costs_factor', {
        type: 'manual',
        message: 'Indirect costs factor must be between 0 and 1'
      });
      return;
    }

    // Operating costs
    if (!data.utility_cost || data.utility_cost <= 0) {
      form.setError('utility_cost', {
        type: 'manual',
        message: 'Utility cost must be positive'
      });
      return;
    }
    if (!data.raw_material_cost || data.raw_material_cost <= 0) {
      form.setError('raw_material_cost', {
        type: 'manual',
        message: 'Raw material cost must be positive'
      });
      return;
    }
    if (!data.labor_cost || data.labor_cost <= 0) {
      form.setError('labor_cost', {
        type: 'manual',
        message: 'Labor cost must be positive'
      });
      return;
    }
    if (!data.maintenance_factor || data.maintenance_factor <= 0 || data.maintenance_factor > 1) {
      form.setError('maintenance_factor', {
        type: 'manual',
        message: 'Maintenance factor must be between 0 and 1'
      });
      return;
    }

    // Financial parameters
    if (!data.project_duration || data.project_duration <= 0) {
      form.setError('project_duration', {
        type: 'manual',
        message: 'Project duration must be positive'
      });
      return;
    }
    if (!data.discount_rate || data.discount_rate <= 0 || data.discount_rate > 1) {
      form.setError('discount_rate', {
        type: 'manual',
        message: 'Discount rate must be between 0 and 1'
      });
      return;
    }
    if (!data.revenue_per_year || data.revenue_per_year <= 0) {
      form.setError('revenue_per_year', {
        type: 'manual',
        message: 'Annual revenue must be positive'
      });
      return;
    }

    onSubmit(data);
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

          <form id="economic-form" onSubmit={form.handleSubmit(handleFormSubmit)} className="space-y-8">
            <div className="grid gap-6">
              <Card className="p-6">
                <FormSection 
                  title="Production Parameters" 
                  tooltip="Configure the production and operational parameters"
                >
                  <div className="grid gap-4 sm:grid-cols-2">
                    <FormNumberInput
                      name="production_volume"
                      label="Production Volume"
                      unit="kg/year"
                      min={0}
                      required
                      tooltip="Annual production capacity"
                    />
                    <FormNumberInput
                      name="operating_hours"
                      label="Operating Hours"
                      unit="h/year"
                      min={0}
                      max={8760}
                      required
                      tooltip="Annual operating hours (max 8760 hours/year)"
                    />
                  </div>
                </FormSection>
              </Card>

              <Card className="p-6">
                <FormSection 
                  title="Equipment Configuration" 
                  tooltip="Configure equipment details and costs"
                >
                  <div className="grid gap-4 sm:grid-cols-2">
                    <FormNumberInput
                      name="equipment.0.cost"
                      label="Equipment Cost"
                      unit="$"
                      min={0}
                      required
                      tooltip="Base cost of main equipment"
                    />
                    <FormNumberInput
                      name="equipment.0.efficiency"
                      label="Equipment Efficiency"
                      unit="ratio"
                      min={0}
                      max={1}
                      step={0.01}
                      required
                      tooltip="Operating efficiency of equipment"
                    />
                    <FormNumberInput
                      name="equipment.0.maintenance_cost"
                      label="Maintenance Cost"
                      unit="$/year"
                      min={0}
                      required
                      tooltip="Annual maintenance cost"
                    />
                    <FormNumberInput
                      name="equipment.0.energy_consumption"
                      label="Energy Consumption"
                      unit="kWh"
                      min={0}
                      required
                      tooltip="Energy consumption of equipment"
                    />
                    <FormNumberInput
                      name="equipment.0.processing_capacity"
                      label="Processing Capacity"
                      unit="kg/h"
                      min={0}
                      required
                      tooltip="Processing capacity of equipment"
                    />
                  </div>
                </FormSection>
              </Card>

              <Card className="p-6">
                <FormSection 
                  title="Resource Configuration" 
                  tooltip="Configure utilities, materials, and labor"
                >
                  <div className="grid gap-4 sm:grid-cols-2">
                    <FormNumberInput
                      name="utilities.0.consumption"
                      label="Utility Consumption"
                      unit="kWh"
                      min={0}
                      required
                      tooltip="Utility consumption rate"
                    />
                    <FormNumberInput
                      name="utilities.0.unit_price"
                      label="Utility Unit Price"
                      unit="$/kWh"
                      min={0}
                      step={0.01}
                      required
                      tooltip="Price per unit of utility"
                    />
                    <FormNumberInput
                      name="raw_materials.0.quantity"
                      label="Raw Material Quantity"
                      unit="kg"
                      min={0}
                      required
                      tooltip="Quantity of raw materials"
                    />
                    <FormNumberInput
                      name="raw_materials.0.unit_price"
                      label="Raw Material Unit Price"
                      unit="$/kg"
                      min={0}
                      step={0.01}
                      required
                      tooltip="Price per unit of raw material"
                    />
                  </div>
                </FormSection>
              </Card>

              <Card className="p-6">
                <FormSection 
                  title="Labor Configuration" 
                  tooltip="Configure labor parameters"
                >
                  <div className="grid gap-4 sm:grid-cols-2">
                    <FormNumberInput
                      name="labor_config.hourly_wage"
                      label="Hourly Wage"
                      unit="$/h"
                      min={0}
                      step={0.01}
                      required
                      tooltip="Hourly wage rate"
                    />
                    <FormNumberInput
                      name="labor_config.hours_per_week"
                      label="Hours per Week"
                      unit="h"
                      min={0}
                      max={168}
                      required
                      tooltip="Working hours per week"
                    />
                    <FormNumberInput
                      name="labor_config.weeks_per_year"
                      label="Weeks per Year"
                      unit="weeks"
                      min={0}
                      max={52}
                      required
                      tooltip="Working weeks per year"
                    />
                    <FormNumberInput
                      name="labor_config.num_workers"
                      label="Number of Workers"
                      unit="workers"
                      min={1}
                      step={1}
                      required
                      tooltip="Number of workers required"
                    />
                  </div>
                </FormSection>
              </Card>

              <Card className="p-6">
                <FormSection 
                  title="Financial Parameters" 
                  tooltip="Configure the financial analysis parameters"
                >
                  <div className="grid gap-4 sm:grid-cols-2">
                    <FormNumberInput
                      name="project_duration"
                      label="Project Duration"
                      unit="years"
                      min={1}
                      max={50}
                      step={1}
                      required
                      tooltip="Expected project lifetime"
                    />
                    <FormNumberInput
                      name="discount_rate"
                      label="Discount Rate"
                      unit="ratio"
                      min={0}
                      max={1}
                      step={0.01}
                      required
                      tooltip="Annual discount rate for NPV calculations"
                    />
                    <FormNumberInput
                      name="revenue_per_year"
                      label="Annual Revenue"
                      unit="$/year"
                      min={0}
                      required
                      tooltip="Expected annual revenue from product sales"
                    />
                  </div>
                </FormSection>
              </Card>
            </div>
          </form>
        </div>
      </FormProvider>
    </TooltipProvider>
  );
}

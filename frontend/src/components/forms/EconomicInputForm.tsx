"use client";

import React from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import * as z from "zod";
import { Button } from "@/components/ui/button";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { ProcessType } from "@/types/process";
import { EconomicParameters } from "@/types/economic";

const economicSchema = z.object({
  process_type: z.enum(["baseline", "rf", "ir"]),
  production_volume: z.number().min(0),
  operating_hours: z.number().min(0),
  equipment_cost: z.number().min(0),
  utility_cost: z.number().min(0),
  raw_material_cost: z.number().min(0),
  labor_cost: z.number().min(0),
  maintenance_factor: z.number().min(0).max(1),
  indirect_costs_factor: z.number().min(0).max(1),
  installation_factor: z.number().min(0).max(1),
  project_duration: z.number().min(1),
  discount_rate: z.number().min(0).max(1),
  revenue_per_year: z.number().min(0)
});

type EconomicFormValues = z.infer<typeof economicSchema>;

interface EconomicInputFormProps {
  onSubmit: (values: EconomicParameters) => void;
  isSubmitting?: boolean;
}

export default function EconomicInputForm({
  onSubmit,
  isSubmitting = false,
}: EconomicInputFormProps) {
  const form = useForm<EconomicFormValues>({
    resolver: zodResolver(economicSchema),
    defaultValues: {
      process_type: "baseline",
      production_volume: 0,
      operating_hours: 0,
      equipment_cost: 0,
      utility_cost: 0,
      raw_material_cost: 0,
      labor_cost: 0,
      maintenance_factor: 0.05,
      indirect_costs_factor: 0.15,
      installation_factor: 0.2,
      project_duration: 1,
      discount_rate: 0.1,
      revenue_per_year: 0
    },
  });

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
        <FormField
          control={form.control}
          name="process_type"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Process Type</FormLabel>
              <Select onValueChange={field.onChange} defaultValue={field.value}>
                <FormControl>
                  <SelectTrigger>
                    <SelectValue placeholder="Select process type" />
                  </SelectTrigger>
                </FormControl>
                <SelectContent>
                  <SelectItem value="baseline">Baseline</SelectItem>
                  <SelectItem value="rf">RF</SelectItem>
                  <SelectItem value="ir">IR</SelectItem>
                </SelectContent>
              </Select>
              <FormMessage />
            </FormItem>
          )}
        />

        <FormField
          control={form.control}
          name="production_volume"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Production Volume (kg/year)</FormLabel>
              <FormControl>
                <Input
                  type="number"
                  {...field}
                  onChange={(e) => field.onChange(Number(e.target.value))}
                />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        <FormField
          control={form.control}
          name="operating_hours"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Operating Hours (h/year)</FormLabel>
              <FormControl>
                <Input
                  type="number"
                  {...field}
                  onChange={(e) => field.onChange(Number(e.target.value))}
                />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        <FormField
          control={form.control}
          name="equipment_cost"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Equipment Cost ($)</FormLabel>
              <FormControl>
                <Input
                  type="number"
                  {...field}
                  onChange={(e) => field.onChange(Number(e.target.value))}
                />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        <FormField
          control={form.control}
          name="utility_cost"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Utility Cost ($/year)</FormLabel>
              <FormControl>
                <Input
                  type="number"
                  {...field}
                  onChange={(e) => field.onChange(Number(e.target.value))}
                />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        <FormField
          control={form.control}
          name="raw_material_cost"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Raw Material Cost ($/year)</FormLabel>
              <FormControl>
                <Input
                  type="number"
                  {...field}
                  onChange={(e) => field.onChange(Number(e.target.value))}
                />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        <FormField
          control={form.control}
          name="labor_cost"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Labor Cost ($/year)</FormLabel>
              <FormControl>
                <Input
                  type="number"
                  {...field}
                  onChange={(e) => field.onChange(Number(e.target.value))}
                />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        <FormField
          control={form.control}
          name="maintenance_factor"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Maintenance Factor (0-1)</FormLabel>
              <FormControl>
                <Input
                  type="number"
                  step="0.01"
                  {...field}
                  onChange={(e) => field.onChange(Number(e.target.value))}
                />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        <FormField
          control={form.control}
          name="indirect_costs_factor"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Indirect Costs Factor (0-1)</FormLabel>
              <FormControl>
                <Input
                  type="number"
                  step="0.01"
                  {...field}
                  onChange={(e) => field.onChange(Number(e.target.value))}
                />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        <FormField
          control={form.control}
          name="installation_factor"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Installation Factor (0-1)</FormLabel>
              <FormControl>
                <Input
                  type="number"
                  step="0.01"
                  {...field}
                  onChange={(e) => field.onChange(Number(e.target.value))}
                />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        <FormField
          control={form.control}
          name="project_duration"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Project Duration (years)</FormLabel>
              <FormControl>
                <Input
                  type="number"
                  {...field}
                  onChange={(e) => field.onChange(Number(e.target.value))}
                />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        <FormField
          control={form.control}
          name="discount_rate"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Discount Rate (0-1)</FormLabel>
              <FormControl>
                <Input
                  type="number"
                  step="0.01"
                  {...field}
                  onChange={(e) => field.onChange(Number(e.target.value))}
                />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        <FormField
          control={form.control}
          name="revenue_per_year"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Revenue per Year ($)</FormLabel>
              <FormControl>
                <Input
                  type="number"
                  {...field}
                  onChange={(e) => field.onChange(Number(e.target.value))}
                />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        <Button type="submit" disabled={isSubmitting}>
          {isSubmitting ? "Processing..." : "Submit Analysis"}
        </Button>
      </form>
    </Form>
  );
}

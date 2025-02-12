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
import { EnvironmentalParameters } from "@/types/environmental";

const environmentalSchema = z.object({
  process_type: z.enum(["baseline", "rf", "ir"]),
  production_volume: z.number().min(0),
  electricity_consumption: z.number().min(0),
  water_consumption: z.number().min(0),
  cooling_consumption: z.number().min(0),
  transport_consumption: z.number().min(0),
  equipment_mass: z.number().min(0),
  thermal_ratio: z.number().min(0).max(1),
  allocation_method: z.enum(["economic", "physical", "hybrid"]),
  hybrid_weights: z.record(z.string(), z.number()).default({})
});

type EnvironmentalFormValues = z.infer<typeof environmentalSchema>;

interface EnvironmentalInputFormProps {
  onSubmit: (values: EnvironmentalParameters) => void;
  isSubmitting?: boolean;
}

export default function EnvironmentalInputForm({
  onSubmit,
  isSubmitting = false,
}: EnvironmentalInputFormProps) {
  const form = useForm<EnvironmentalFormValues>({
    resolver: zodResolver(environmentalSchema),
    defaultValues: {
      process_type: "baseline",
      production_volume: 0,
      electricity_consumption: 0,
      water_consumption: 0,
      cooling_consumption: 0,
      transport_consumption: 0,
      equipment_mass: 0,
      thermal_ratio: 0.3,
      allocation_method: "hybrid",
      hybrid_weights: {}
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
          name="electricity_consumption"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Electricity Consumption (kWh)</FormLabel>
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
          name="water_consumption"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Water Consumption (m³)</FormLabel>
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
          name="cooling_consumption"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Cooling Consumption (kWh)</FormLabel>
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
          name="transport_consumption"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Transport Energy (MJ)</FormLabel>
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
          name="equipment_mass"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Equipment Mass (kg)</FormLabel>
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
          name="thermal_ratio"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Thermal Ratio (0-1)</FormLabel>
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
          name="allocation_method"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Allocation Method</FormLabel>
              <Select onValueChange={field.onChange} defaultValue={field.value}>
                <FormControl>
                  <SelectTrigger>
                    <SelectValue placeholder="Select allocation method" />
                  </SelectTrigger>
                </FormControl>
                <SelectContent>
                  <SelectItem value="economic">Economic</SelectItem>
                  <SelectItem value="physical">Physical</SelectItem>
                  <SelectItem value="hybrid">Hybrid</SelectItem>
                </SelectContent>
              </Select>
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

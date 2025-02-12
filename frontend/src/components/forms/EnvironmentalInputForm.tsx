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

const environmentalSchema = z.object({
  energyConsumption: z.number().min(0),
  waterConsumption: z.number().min(0),
  wasteGeneration: z.number().min(0),
  co2Emissions: z.number().min(0),
  recyclingRate: z.number().min(0).max(100),
});

type EnvironmentalFormValues = z.infer<typeof environmentalSchema>;

interface EnvironmentalInputFormProps {
  onSubmit: (values: EnvironmentalFormValues) => void;
  isSubmitting?: boolean;
}

export default function EnvironmentalInputForm({
  onSubmit,
  isSubmitting = false,
}: EnvironmentalInputFormProps) {
  const form = useForm<EnvironmentalFormValues>({
    resolver: zodResolver(environmentalSchema),
    defaultValues: {
      energyConsumption: 0,
      waterConsumption: 0,
      wasteGeneration: 0,
      co2Emissions: 0,
      recyclingRate: 0,
    },
  });

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
        <FormField
          control={form.control}
          name="energyConsumption"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Energy Consumption (kWh)</FormLabel>
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
          name="waterConsumption"
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
          name="wasteGeneration"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Waste Generation (kg)</FormLabel>
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
          name="co2Emissions"
          render={({ field }) => (
            <FormItem>
              <FormLabel>CO₂ Emissions (kg)</FormLabel>
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
          name="recyclingRate"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Recycling Rate (%)</FormLabel>
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

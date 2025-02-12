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

const economicSchema = z.object({
  capitalCost: z.number().min(0),
  operatingCost: z.number().min(0),
  laborCost: z.number().min(0),
  maintenanceCost: z.number().min(0),
  productionRate: z.number().min(0),
  sellingPrice: z.number().min(0),
});

type EconomicFormValues = z.infer<typeof economicSchema>;

interface EconomicInputFormProps {
  onSubmit: (values: EconomicFormValues) => void;
  isSubmitting?: boolean;
}

export default function EconomicInputForm({
  onSubmit,
  isSubmitting = false,
}: EconomicInputFormProps) {
  const form = useForm<EconomicFormValues>({
    resolver: zodResolver(economicSchema),
    defaultValues: {
      capitalCost: 0,
      operatingCost: 0,
      laborCost: 0,
      maintenanceCost: 0,
      productionRate: 0,
      sellingPrice: 0,
    },
  });

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
        <FormField
          control={form.control}
          name="capitalCost"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Capital Cost ($)</FormLabel>
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
          name="operatingCost"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Operating Cost ($/year)</FormLabel>
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
          name="laborCost"
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
          name="maintenanceCost"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Maintenance Cost ($/year)</FormLabel>
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
          name="productionRate"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Production Rate (kg/year)</FormLabel>
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
          name="sellingPrice"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Selling Price ($/kg)</FormLabel>
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

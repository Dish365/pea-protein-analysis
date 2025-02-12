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
import { Card } from "@/components/ui/card";
import { Tooltip, TooltipContent, TooltipTrigger } from "@/components/ui/tooltip";
import { Info } from "lucide-react";
import { TechnicalParameters } from "@/types/technical";
import { formatNumber } from "@/lib/formatters";
import { ProcessType, ProcessTypeValues } from "@/types/process";

const technicalSchema = z.object({
  processType: z.enum(['baseline', 'rf', 'ir'] as const),
  airFlow: z.number().min(0).max(1000),
  classifierSpeed: z.number().min(0),
  
  // Mass Balance
  inputMass: z.number().min(0).max(10000),
  outputMass: z.number().min(0).max(10000),
  
  // Content Analysis
  initialProteinContent: z.number().min(0).max(100),
  finalProteinContent: z.number().min(0).max(100),
  initialMoistureContent: z.number().min(0).max(100),
  finalMoistureContent: z.number().min(0).max(100),
  
  // Particle Size Analysis
  d10ParticleSize: z.number().min(0),
  d50ParticleSize: z.number().min(0),
  d90ParticleSize: z.number().min(0)
});

type TechnicalFormValues = z.infer<typeof technicalSchema>;

interface TechnicalInputFormProps {
  onSubmit: (values: TechnicalParameters) => void;
  isSubmitting?: boolean;
}

export default function TechnicalInputForm({
  onSubmit,
  isSubmitting = false,
}: TechnicalInputFormProps) {
  const form = useForm<TechnicalFormValues>({
    resolver: zodResolver(technicalSchema),
    defaultValues: {
      processType: "baseline",
      airFlow: 0,
      classifierSpeed: 0,
      inputMass: 0,
      outputMass: 0,
      initialProteinContent: 0,
      finalProteinContent: 0,
      initialMoistureContent: 0,
      finalMoistureContent: 0,
      d10ParticleSize: 0,
      d50ParticleSize: 0,
      d90ParticleSize: 0
    }
  });

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
        <Card className="p-6">
          <h3 className="text-lg font-medium mb-4">Process Parameters</h3>
          <div className="space-y-4">
            <FormField
              control={form.control}
              name="processType"
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
              name="airFlow"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Air Flow Rate (m³/h)</FormLabel>
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
              name="classifierSpeed"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Classifier Speed (rpm)</FormLabel>
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
          </div>
        </Card>

        <Card className="p-6">
          <h3 className="text-lg font-medium mb-4">Mass Balance</h3>
          <div className="space-y-4">
            <FormField
              control={form.control}
              name="inputMass"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Input Mass (kg)</FormLabel>
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
              name="outputMass"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Output Mass (kg)</FormLabel>
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
          </div>
        </Card>

        <Card className="p-6">
          <h3 className="text-lg font-medium mb-4">Content Analysis</h3>
          <div className="space-y-4">
            <FormField
              control={form.control}
              name="initialProteinContent"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Initial Protein Content (%)</FormLabel>
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
              name="finalProteinContent"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Final Protein Content (%)</FormLabel>
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
              name="initialMoistureContent"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Initial Moisture Content (%)</FormLabel>
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
              name="finalMoistureContent"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Final Moisture Content (%)</FormLabel>
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
          </div>
        </Card>

        <Card className="p-6">
          <h3 className="text-lg font-medium mb-4">Particle Size Analysis</h3>
          <div className="space-y-4">
            <FormField
              control={form.control}
              name="d10ParticleSize"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>D10 Particle Size (μm)</FormLabel>
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
              name="d50ParticleSize"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>D50 Particle Size (μm)</FormLabel>
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
              name="d90ParticleSize"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>D90 Particle Size (μm)</FormLabel>
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
          </div>
        </Card>

        <div className="flex justify-end">
          <Button type="submit" disabled={isSubmitting}>
            {isSubmitting ? "Submitting..." : "Next"}
          </Button>
        </div>
      </form>
    </Form>
  );
}

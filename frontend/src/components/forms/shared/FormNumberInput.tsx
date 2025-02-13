import React from 'react';
import { useFormContext } from "react-hook-form";
import {
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { Tooltip, TooltipContent, TooltipTrigger } from "@/components/ui/tooltip";
import { Info } from "lucide-react";

interface FormNumberInputProps {
  name: string;
  label: string;
  tooltip?: string;
  unit?: string;
  min?: number;
  max?: number;
  step?: number;
  required?: boolean;
}

export function FormNumberInput({
  name,
  label,
  tooltip,
  unit,
  min,
  max,
  step = 0.01,
  required = false,
}: FormNumberInputProps) {
  const form = useFormContext();

  return (
    <FormField
      control={form.control}
      name={name}
      render={({ field }) => (
        <FormItem>
          <div className="flex items-center gap-2">
            <FormLabel className={required ? "after:content-['*'] after:ml-0.5 after:text-red-500" : ""}>
              {label}
            </FormLabel>
            {tooltip && (
              <Tooltip>
                <TooltipTrigger asChild>
                  <Info className="h-4 w-4 text-muted-foreground cursor-help" />
                </TooltipTrigger>
                <TooltipContent>
                  <p className="max-w-xs">{tooltip}</p>
                </TooltipContent>
              </Tooltip>
            )}
          </div>
          <div className="relative">
            <FormControl>
              <Input
                type="number"
                inputMode="decimal"
                min={min}
                max={max}
                step={step}
                {...field}
                onChange={(e) => {
                  const value = e.target.value === '' ? '' : Number(e.target.value);
                  field.onChange(value);
                }}
                className={unit ? "pr-12" : ""}
              />
            </FormControl>
            {unit && (
              <div className="absolute inset-y-0 right-0 flex items-center pr-3 pointer-events-none text-sm text-muted-foreground">
                {unit}
              </div>
            )}
          </div>
          <FormMessage />
        </FormItem>
      )}
    />
  );
} 
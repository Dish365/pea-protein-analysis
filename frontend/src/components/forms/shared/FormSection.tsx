import React from 'react';
import { Card } from "@/components/ui/card";
import { Tooltip, TooltipContent, TooltipTrigger } from "@/components/ui/tooltip";
import { Info } from "lucide-react";

interface FormSectionProps {
  title: string;
  description?: string;
  children: React.ReactNode;
  tooltip?: string;
}

export function FormSection({
  title,
  description,
  children,
  tooltip
}: FormSectionProps) {
  return (
    <div className="space-y-4">
      <div className="space-y-1">
        <div className="flex items-center gap-2">
          <h3 className="text-lg font-semibold tracking-tight">{title}</h3>
          {tooltip && (
            <Tooltip>
              <TooltipTrigger asChild>
                <Info className="h-4 w-4 text-muted-foreground cursor-help opacity-70 hover:opacity-100 transition-opacity" />
              </TooltipTrigger>
              <TooltipContent side="right" align="start" className="max-w-xs">
                <p className="text-sm">{tooltip}</p>
              </TooltipContent>
            </Tooltip>
          )}
        </div>
        {description && (
          <p className="text-sm text-muted-foreground">{description}</p>
        )}
      </div>
      <div className="space-y-4">
        {children}
      </div>
    </div>
  );
} 
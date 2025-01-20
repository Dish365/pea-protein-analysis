"use client";

import { useState } from "react";
import { z } from "zod";

const economicInputSchema = z.object({
  capitalCosts: {
    equipment: z.number().positive(),
    installation: z.number().positive(),
    facilities: z.number().positive(),
  },
  operatingCosts: {
    labor: z.number().positive(),
    utilities: z.number().positive(),
    maintenance: z.number().positive(),
    materials: z.number().positive(),
  },
  financialParameters: {
    discountRate: z.number().min(0).max(100),
    projectLife: z.number().positive(),
    taxRate: z.number().min(0).max(100),
  },
});

export function EconomicInputForm() {
  const [formData, setFormData] = useState({
    capitalCosts: {
      equipment: 0,
      installation: 0,
      facilities: 0,
    },
    operatingCosts: {
      labor: 0,
      utilities: 0,
      maintenance: 0,
      materials: 0,
    },
    financialParameters: {
      discountRate: 0,
      projectLife: 0,
      taxRate: 0,
    },
  });

  return (
    <div className="space-y-6">
      <div>
        <h3 className="text-lg font-semibold mb-4">Capital Costs</h3>
        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700">
              Equipment Cost ($)
            </label>
            <input
              type="number"
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
              value={formData.capitalCosts.equipment}
              onChange={(e) =>
                setFormData({
                  ...formData,
                  capitalCosts: {
                    ...formData.capitalCosts,
                    equipment: parseFloat(e.target.value),
                  },
                })
              }
            />
          </div>
          {/* Add other capital cost inputs */}
        </div>
      </div>

      {/* Add Operating Costs and Financial Parameters sections */}
    </div>
  );
}

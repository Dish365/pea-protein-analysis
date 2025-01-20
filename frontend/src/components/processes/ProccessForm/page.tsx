'use client'

import { useState } from 'react'
import { z } from 'zod'

const processSchema = z.object({
  name: z.string().min(1),
  type: z.enum(['baseline', 'rf', 'ir']),
  technicalParams: z.object({
    inputMass: z.number().positive(),
    proteinContent: z.number().min(0).max(100),
    moistureContent: z.number().min(0).max(100),
    particleSize: z.number().positive(),
  }),
  economicParams: z.object({
    equipmentCost: z.number().positive(),
    operatingCost: z.number().positive(),
    laborCost: z.number().positive(),
  }),
})

export function ProcessForm() {
  const [step, setStep] = useState(1)

  return (
    <form className="space-y-6">
      {step === 1 && (
        <div className="space-y-4">
          <h2 className="text-lg font-semibold">Basic Information</h2>
          
          <div>
            <label className="block text-sm font-medium text-gray-700">
              Process Name
            </label>
            <input
              type="text"
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700">
              Process Type
            </label>
            <select className="mt-1 block w-full rounded-md border-gray-300 shadow-sm">
              <option value="baseline">Baseline</option>
              <option value="rf">RF Treatment</option>
              <option value="ir">IR Treatment</option>
            </select>
          </div>
        </div>
      )}

      {step === 2 && (
        <div className="space-y-4">
          <h2 className="text-lg font-semibold">Technical Parameters</h2>
          
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700">
                Input Mass (kg)
              </label>
              <input
                type="number"
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700">
                Protein Content (%)
              </label>
              <input
                type="number"
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
              />
            </div>
          </div>
        </div>
      )}

      <div className="flex justify-between pt-4">
        {step > 1 && (
          <button
            type="button"
            onClick={() => setStep(step - 1)}
            className="px-4 py-2 border rounded-md"
          >
            Previous
          </button>
        )}
        {step < 3 ? (
          <button
            type="button"
            onClick={() => setStep(step + 1)}
            className="px-4 py-2 bg-blue-600 text-white rounded-md"
          >
            Next
          </button>
        ) : (
          <button
            type="submit"
            className="px-4 py-2 bg-green-600 text-white rounded-md"
          >
            Start Analysis
          </button>
        )}
      </div>
    </form>
  )
}
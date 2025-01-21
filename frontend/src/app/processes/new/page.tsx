"use client";

import { useState } from "react";
import { TechnicalInputForm } from "@/components/forms/ProcessInput/TechnicalInputForm";
import { EconomicInputForm } from "@/components/forms/ProcessInput/EconomicInputForm";
import { EnvironmentalInputForm } from "@/components/forms/ProcessInput/EnvironmentalInputForm";
import Steps from "@/components/ui/Steps";

export default function NewProcessPage() {
  const [activeStep, setActiveStep] = useState(1);

  // Define the handleSubmit function
  const handleSubmit = () => {
    // Add your form submission logic here
    console.log("Form submitted");
  };

  return (
    <div className="max-w-4xl mx-auto py-8">
      <div className="mb-8">
        <h1 className="text-2xl font-bold">New Process Analysis</h1>
        <p className="text-gray-600">Enter process parameters for analysis</p>
      </div>

      {/* Progress Steps */}
      <div className="mb-8">
        <Steps currentStep={activeStep} />
      </div>

      {/* Form Content */}
      <div className="bg-white rounded-lg shadow-sm p-6">
        {activeStep === 1 && <TechnicalInputForm />}
        {activeStep === 2 && <EconomicInputForm />}
        {activeStep === 3 && <EnvironmentalInputForm />}

        {/* Navigation Buttons */}
        <div className="mt-6 flex justify-between">
          <button
            onClick={() => setActiveStep(Math.max(1, activeStep - 1))}
            disabled={activeStep === 1}
            className="px-4 py-2 border rounded-md"
          >
            Previous
          </button>
          <button
            onClick={() =>
              activeStep === 3 ? handleSubmit() : setActiveStep(activeStep + 1)
            }
            className="px-4 py-2 bg-blue-600 text-white rounded-md"
          >
            {activeStep === 3 ? "Start Analysis" : "Next"}
          </button>
        </div>
      </div>
    </div>
  );
}

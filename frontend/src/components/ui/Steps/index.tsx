import React from "react";

interface StepsProps {
  currentStep: number;
}

const Steps: React.FC<StepsProps> = ({ currentStep }) => {
  const steps = ["Step 1", "Step 2", "Step 3"]; // Define your steps here

  return (
    <div className="steps-container">
      {steps.map((step, index) => (
        <div
          key={index}
          className={`step ${index + 1 === currentStep ? "active" : ""}`}
        >
          {step}
        </div>
      ))}
    </div>
  );
};

export default Steps;

import React from "react";

interface ProcessFormProps {
  onSubmit: (data: ProcessData) => void;
}

interface ProcessData {
  name: string;
  description: string;
  parameters: {
    temperature: number;
    pressure: number;
    duration: number;
  };
}

export function ProcessForm({ onSubmit }: ProcessFormProps) {
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit({
      name: "",
      description: "",
      parameters: {
        temperature: 0,
        pressure: 0,
        duration: 0,
      },
    });
  };

  return <form onSubmit={handleSubmit}>{/* Form fields will go here */}</form>;
}

export default function NewProcessPage() {
  return (
    <div className="max-w-2xl mx-auto">
      <h1 className="text-2xl font-bold mb-6">New Process Analysis</h1>

      <div className="bg-white rounded-lg shadow p-6">
        <ProcessForm onSubmit={(data) => console.log(data)} />
      </div>
    </div>
  );
}

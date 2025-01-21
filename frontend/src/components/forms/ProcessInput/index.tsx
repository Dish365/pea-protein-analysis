import ProcessForm from "@/components/processes/ProcessForm";

export default function NewProcessPage() {
  return (
    <div className="max-w-2xl mx-auto">
      <h1 className="text-2xl font-bold mb-6">New Process Analysis</h1>

      <div className="bg-white rounded-lg shadow p-6">
        <ProcessForm />
      </div>
    </div>
  );
}

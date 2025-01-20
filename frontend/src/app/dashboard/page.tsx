import { ProcessCard } from '@/components/ui/Card'
import { DataTable } from '@/components/ui/DataTable'

export default function DashboardPage() {
  return (
    <div className="space-y-8">
      <h1 className="text-3xl font-bold">Process Analysis Dashboard</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <ProcessCard
          title="Technical Analysis"
          metric="Protein Recovery"
          value="85%"
          trend="+2.5%"
        />
        <ProcessCard
          title="Economic Analysis"
          metric="ROI"
          value="127%"
          trend="+5.3%"
        />
        <ProcessCard
          title="Environmental Analysis"
          metric="Eco-efficiency"
          value="92"
          trend="-1.2%"
        />
      </div>

      <div className="bg-white rounded-lg shadow">
        <h2 className="text-xl font-semibold p-4 border-b">Recent Processes</h2>
        <DataTable />
      </div>
    </div>
  )
}
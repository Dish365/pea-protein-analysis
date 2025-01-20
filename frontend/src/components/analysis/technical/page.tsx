import { Suspense } from 'react';
import { ProteinRecoveryChart } from '@/components/analysis/technical/ProteinRecoveryCard';
import { EfficiencyMetrics } from '@/components/analysis/technical/EfficiencyMetrics';
import { ParticleSizeDisplay } from '@/components/analysis/technical/ParticleSizeDisplay';

export default function TechnicalAnalysisPage() {
  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Technical Analysis Dashboard</h1>
      
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-lg font-semibold mb-4">Protein Recovery Analysis</h2>
          <Suspense fallback={<ChartSkeleton />}>
            <ProteinRecoveryChart />
          </Suspense>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-lg font-semibold mb-4">Process Efficiency</h2>
          <Suspense fallback={<ChartSkeleton />}>
            <EfficiencyMetrics />
          </Suspense>
        </div>

        <div className="bg-white rounded-lg shadow p-6 lg:col-span-2">
          <h2 className="text-lg font-semibold mb-4">Particle Size Distribution</h2>
          <Suspense fallback={<ChartSkeleton />}>
            <ParticleSizeDisplay />
          </Suspense>
        </div>
      </div>
    </div>
  );
}

function ChartSkeleton() {
  return <div className="h-[300px] bg-gray-100 animate-pulse rounded-lg" />;
}
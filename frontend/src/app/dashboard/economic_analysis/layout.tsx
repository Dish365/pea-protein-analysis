import React from 'react';

export default function AnalysisLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="flex-1 space-y-4 p-4 md:p-8 pt-6 bg-muted/5 min-h-screen animate-in fade-in duration-300">
      {children}
    </div>
  );
}

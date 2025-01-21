import React from "react";
import ReactFlow, {
  Node,
  Edge,
  Controls,
  Background,
  MiniMap,
} from "reactflow";
import "reactflow/dist/style.css";

interface ProcessFlowProps {
  nodes: Array<{
    id: string;
    label: string;
    type?: "input" | "default" | "output";
    position: { x: number; y: number };
    data?: Record<string, unknown>;
  }>;
  edges: Array<{
    id: string;
    source: string;
    target: string;
    label?: string;
    animated?: boolean;
  }>;
  onNodeClick?: (node: Node) => void;
  onEdgeClick?: (edge: Edge) => void;
}

const ProcessFlow: React.FC<ProcessFlowProps> = ({
  nodes,
  edges,
  onNodeClick,
  onEdgeClick,
}) => {
  const processNodes = nodes.map((node) => ({
    id: node.id,
    type: node.type || "default",
    position: node.position,
    data: { label: node.label, ...node.data },
  }));

  return (
    <div className="process-flow-container h-[600px] w-full">
      <ReactFlow
        nodes={processNodes}
        edges={edges}
        onNodeClick={(_, node) => onNodeClick?.(node)}
        onEdgeClick={(_, edge) => onEdgeClick?.(edge)}
        fitView
      >
        <Background />
        <Controls />
        <MiniMap />
      </ReactFlow>
    </div>
  );
};

export default ProcessFlow;

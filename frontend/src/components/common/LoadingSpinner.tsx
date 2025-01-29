import { Spin } from "antd";
import React from "react";

interface LoadingSpinnerProps {
  tip?: string;
}

const LoadingSpinner: React.FC<LoadingSpinnerProps> = ({
  tip = "Loading...",
}) => {
  return (
    <div
      className="loading-container"
      style={{
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        height: "100vh",
        width: "100%",
        position: "fixed",
        top: 0,
        left: 0,
        background: "rgba(255, 255, 255, 0.9)",
        zIndex: 1000,
      }}
    >
      <Spin size="large" tip={tip} />
    </div>
  );
};

export default LoadingSpinner;

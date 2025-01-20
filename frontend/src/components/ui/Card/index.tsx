import React from "react";

interface CardProps {
  children: React.ReactNode;
  className?: string;
}

const Card: React.FC<CardProps> = ({ children, className = "" }) => {
  return (
    <div className={`rounded-lg shadow-md bg-white p-4 ${className}`}>
      {children}
    </div>
  );
};

export default Card;

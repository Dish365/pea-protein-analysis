"use client";

import React, { useState } from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer
} from "recharts";

const OpexPage = () => {
  const [opexData] = useState([
    {
      category: "Utilities",
      cost: 150000,
    },
    {
      category: "Raw Materials",
      cost: 300000,
    },
    {
      category: "Labor",
      cost: 200000,
    },
    {
      category: "Maintenance",
      cost: 100000,
    },
    {
      category: "Other",
      cost: 50000,
    },
  ]);

  const totalOpex = opexData.reduce((sum, item) => sum + item.cost, 0);

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">OPEX Analysis</h1>
      
      <div className="bg-white rounded-lg shadow-lg p-6 mb-6">
        <h2 className="text-xl font-semibold mb-4">Total OPEX: ${(totalOpex).toLocaleString()}</h2>
        
        <div className="h-[400px] mb-8">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={opexData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="category" />
              <YAxis 
                tickFormatter={(value) => `$${(value/1000).toFixed(1)}k`}
              />
              <Tooltip 
                formatter={(value) => [`$${(value).toLocaleString()}`, "Cost"]}
              />
              <Bar dataKey="cost" fill="#10B981" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {opexData.map((item) => (
            <div key={item.category} className="bg-gray-50 rounded-lg p-4">
              <h3 className="text-lg font-medium text-gray-900">{item.category}</h3>
              <p className="text-2xl font-bold text-green-600">
                ${item.cost.toLocaleString()}
              </p>
              <p className="text-sm text-gray-500">
                {((item.cost / totalOpex) * 100).toFixed(1)}% of total
              </p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default OpexPage;

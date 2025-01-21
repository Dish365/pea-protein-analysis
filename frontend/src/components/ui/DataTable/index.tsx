import React from "react";

interface Column {
  header: string;
  accessor: string; // or whatever type your accessor is
}

interface DataTableProps<T> {
  data: T[];
  columns: Column[];
}

export const DataTable = <T extends Record<string, unknown>>({
  data,
  columns,
}: DataTableProps<T>) => {
  return (
    <div className="data-table-container">
      <table>
        <thead>
          <tr>
            {columns.map((column, index) => (
              <th key={index}>{column.header}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {data.map((row, rowIndex) => (
            <tr key={rowIndex}>
              {columns.map((column, colIndex) => (
                <td key={colIndex}>{String(row[column.accessor])}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default DataTable;

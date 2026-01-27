import React from "react";
import { Pie } from "react-chartjs-2";

function Dashboards({ summary }) {
  if (!summary) return null;

  const typeData = {
    labels: Object.keys(summary.type_distribution),
    datasets: [
      {
        label: "Equipment Count",
        data: Object.values(summary.type_distribution),
      },
    ],
  };

  return (
    <div>
      <h3>Summary</h3>
      <pre>{JSON.stringify(summary, null, 2)}</pre>

      <h3>Type Distribution</h3>
      <Pie data={typeData} />
    </div>
  );
}

export default Dashboards;

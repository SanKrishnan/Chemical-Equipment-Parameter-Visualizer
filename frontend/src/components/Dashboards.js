import React from "react";
import { Pie } from "react-chartjs-2";
import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend
} from "chart.js";

// Register required chart elements
ChartJS.register(ArcElement, Tooltip, Legend);

function Dashboards({ summary }) {
  if (!summary) return null;

  const typeData = {
    labels: Object.keys(summary.type_distribution),
    datasets: [
      {
        label: "Equipment Count",
        data: Object.values(summary.type_distribution),
        backgroundColor: [
          "rgba(233, 0, 50, 0.7)",
          "rgba(0, 153, 255, 0.7)",
          "rgba(255, 183, 0, 0.7)",
          "rgba(0, 255, 255, 0.7)",
          "rgba(85, 0, 255, 0.7)",
          "rgba(255, 128, 0, 0.7)",
        ],
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

import React from "react";
import { Pie } from "react-chartjs-2";
import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend
} from "chart.js";

ChartJS.register(ArcElement, Tooltip, Legend);

function Dashboards({ summary }) {
  if (!summary) {
    return <h3 style={{ textAlign: "center", color: "#555", marginTop:"20px"}}>Upload a CSV to view dashboard</h3>;
  }
  const typeData = {
    labels: Object.keys(summary.type_distribution),
    datasets: [
      {
        label: "Equipment Count",
        data: Object.values(summary.type_distribution),
        backgroundColor: [
          "rgba(255, 0, 55, 0.8)",
          "rgba(0, 153, 255, 0.85)",
          "rgba(255, 183, 0, 0.8)",
          "rgba(0, 255, 255, 0.77)",
          "rgba(85, 0, 255, 0.82)",
          "rgba(255, 128, 0, 0.85)",
        ],
      },
    ],
  };

  return (
    <div style={{ padding: "20px" }}>
      <h2>Dashboard Summary</h2>

      <section style={{ marginBottom: "20px" }}>
        <h3>Summary Data</h3>
        <pre style={{ background: "#cdcdcd",padding: "12px",borderRadius: "6px", overflowX: "auto", textAlign: "center"}}>
          {JSON.stringify(summary, null, 2)}
        </pre>
      </section>

      {/* Distribution Chart */}
      <section>
        <h3>Type Distribution</h3>
        <div style={{ width: "350px", margin: "auto" }}>
          <Pie data={typeData} />
        </div>
      </section>
    </div>
  );
}

export default Dashboards;

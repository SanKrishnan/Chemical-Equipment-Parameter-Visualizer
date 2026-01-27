import React, { useState } from "react";
import CSVUploads from "./components/CSVUploads";
import Dashboards from "./components/Dashboards";

function App() {
  const [summary, setSummary] = useState(null);

  return (
    <div className="App">
      <h1>Chemical Equipment Parameter Visualizer</h1>

      <CSVUpload onSummaryLoad={setSummary} />

      <Dashboard summary={summary} />
    </div>
  );
}

export default App;

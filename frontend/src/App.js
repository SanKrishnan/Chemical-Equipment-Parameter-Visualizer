import React, { useState } from "react";
import CSVUploads from "./components/CSVUploads";
import Dashboards from "./components/Dashboards";
import Login from "./components/Login";
import History from "./components/History";

function App() {
  const [page, setPage] = useState("login");
  const [summary, setSummary] = useState(null);

  return (
    <div className="App">

      <h1>Chemical Equipment Parameter Visualizer</h1>

      {/* Navigation */}
      <button onClick={() => setPage("login")}>Login</button>
      <button onClick={() => setPage("upload")}>Upload CSV</button>
      <button onClick={() => setPage("history")}>History</button>

      {/* Pages */}
      {page === "login" && <Login />}

      {page === "upload" && (
        <>
          <CSVUploads onSummaryLoad={setSummary} />
          <Dashboards summary={summary} />
        </>
      )}

      {page === "history" && <History />}
    </div>
  );
}

export default App;

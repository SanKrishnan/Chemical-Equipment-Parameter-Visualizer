import React, { useState } from "react";
import CSVUploads from "./components/CSVUploads";
import Dashboards from "./components/Dashboards";
import Login from "./components/Login";
import History from "./components/History";

function App() {
  const [summary, setSummary] = useState(null);
  const [page, setPage] = useState("login");

  const handleLoginSuccess = () => {
    setPage("upload");
  };

  return (
    <div className="App">
      <h2 className="upload_title">Upload Equipment CSV</h2>
      <div className="navigate">
        <button onClick={() => setPage("upload")}>Upload</button>
        <button onClick={() => setPage("history")}>History</button>
        <button onClick={() => setPage("dashboard")}>Dashboard</button>
      </div>

      {page === "login" && <Login onLoginSuccess={handleLoginSuccess} />}

      {page === "upload" && (
        <>
          <div style={{ justifyContent: "space-between", alignItems: "flex-start", gap: "40px", padding: "20px"}}>
            <CSVUploads onSummaryLoad={setSummary} setPage={setPage} />
            <Dashboards summary={summary} />
          </div>
        </>
      )}

      {page === "dashboard" && (
        <Dashboards summary={summary} />
      )}

      {page === "history" && <History />}
    </div>
  );
}

export default App;


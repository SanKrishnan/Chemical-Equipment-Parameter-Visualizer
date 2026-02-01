import React, { useState } from "react";
import CSVUploads from "./components/CSVUploads";
import Dashboards from "./components/Dashboards";
import Login from "./components/Login";
import History from "./components/History";
import "./App.css";
function App() {
  const [page, setPage] = useState("login");
  const [summary, setSummary] = useState(null);

  return (
    <div className="App">
      
      <h1 className="title" >Chemical Equipment Parameter Visualizer</h1>
      <div className="navigate">
        <button onClick={() => setPage("login")}>Login</button>
        <button onClick={() => setPage("upload")}>Upload CSV</button>
        <button onClick={() => setPage("history")}>History</button>
      </div>

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

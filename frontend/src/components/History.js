import React, { useEffect, useState } from "react";
import axios from "axios";

function History() {
  const [historyData, setHistoryData] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    fetchHistory();
  }, []);

  const fetchHistory = async () => {
    const token = localStorage.getItem("token");

    if (!token) {
      setError("You must login first.");
      return;
    }

    try {
      const response = await axios.get(
        "http://127.0.0.1:8000/api/history/",
        {
          headers: {
            "Authorization": `Bearer ${token}`
          }
        }
      );

      setHistoryData(response.data);
    } catch (err) {
      console.error(err);
      setError("Could not load history. Token may be expired.");
    }
  };

  return (
    <div>
      <h2 className="d-flex justify-content-center align-items-center #582417" style={{ minHeight: "34vh" }}>Upload History (Last 5 CSV Files)</h2>

      {error && <p style={{ color: "red" }}>{error}</p>}

      {historyData.length === 0 && !error && <p>No uploads found.</p>}

      {historyData.map((item) => (
        <div 
          key={item.id} 
          style={{ 
            border: "1px solid gray", 
            padding: "10px", 
            marginBottom: "10px",
            borderRadius: "8px"
          }}
        >
          <p><strong>File:</strong> {item.file}</p>
          <p><strong>Uploaded At:</strong> {new Date(item.uploaded_at).toLocaleString()}</p>
          
          <h4>Summary:</h4>
          <pre>{JSON.stringify(item.summary, null, 2)}</pre>
        </div>
      ))}
    </div>
  );
}

export default History;

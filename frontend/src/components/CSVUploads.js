import React, { useState } from "react";
import axios from "axios";

function CSVUploads(csvfile) {
  const [file, setFile] = useState(null);
  const [summary, setSummary] = useState(null);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
  if (!file) {
    alert("Please upload a CSV file");
    return;
  }

  const token = localStorage.getItem("token");
  if (!token) {
    alert("Please login first to get a token");
    return;
  }

  const formData = new FormData();
  formData.append("file", file);

  try {
    const response = await axios.post(
      "http://127.0.0.1:8000/api/upload/",
      formData,
      {
        headers: {
          "Content-Type": "multipart/form-data",
          "Authorization": `Bearer ${token}`   // <-- IMPORTANT
        }
      }
    );

    setSummary(response.data.summary);
    csvfile.onSummaryLoad(response.data.summary);

  } catch (error) {
    console.error(error);
    alert("Upload failed. Maybe token expired or incorrect.");
  }
};


  return (
    <div>
      <h2 className="upload_title">Upload Equipment CSV</h2>
      <div className="upload_option">
        <input type="file" onChange={handleFileChange} />
        <button onClick={handleUpload}>Upload</button>
      </div>
      {summary && (
        <div className="summary">
          <h3>Summary</h3>
          <pre>{JSON.stringify(summary, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}

export default CSVUploads;

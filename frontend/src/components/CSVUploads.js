import React, { useState } from "react";
import axios from "axios";

function CSVUploads() {
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

    const formData = new FormData();
    formData.append("file", file);

    const response = await axios.post(
      "http://127.0.0.1:8000/api/upload/",
      formData,
      { headers: { "Content-Type": "multipart/form-data" } }
    );

    setSummary(response.data.summary);
  };

  return (
    <div>
      <h2>Upload Equipment CSV</h2>

      <input type="file" onChange={handleFileChange} />

      <button onClick={handleUpload}>Upload</button>

      {summary && (
        <div>
          <h3>Summary</h3>
          <pre>{JSON.stringify(summary, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}

export default CSVUploads;

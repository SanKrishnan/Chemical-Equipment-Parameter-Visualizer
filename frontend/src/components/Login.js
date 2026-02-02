import React, { useState } from "react";
import axios from "axios";
import "bootstrap-icons/font/bootstrap-icons.css";

function Login({ onLoginSuccess }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const handleLogin = async () => {
    try {
      const response = await axios.post("http://127.0.0.1:8000/api/token/", {
        username,
        password,
      });

      localStorage.setItem("token", response.data.access);
      alert("Login successful!");
      onLoginSuccess();
    } 
    catch (err) {
      alert("Invalid credentials");
    }
  };

  return (
    <div className="d-flex justify-content-center align-items-center" style={{ minHeight: "65vh" }}>
      <div className="card shadow p-4" style={{ width: "350px" }}>
      <h3 className="text-center mb-4">Login</h3>

      <div className="input-group mb-3">
        <span className="input-group-text"><i className="bi bi-person-fill"></i></span>
        <input type="text" className="form-control" placeholder="Enter Username" value={username} onChange={(e) => setUsername(e.target.value)}/>
      </div>

      <div className="input-group mb-3"><span className="input-group-text"><i className="bi bi-lock-fill"></i></span>
        <input type="password" className="form-control" placeholder="Enter Password" value={password} onChange={(e) => setPassword(e.target.value)}/>
      </div>
        <button type="button" className="btn btn-primary w-100" onClick={handleLogin}>Login</button>
      </div>
    </div>
  );
}

export default Login;

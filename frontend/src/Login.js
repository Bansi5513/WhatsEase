// frontend/src/Login.js
import React, {useState} from "react";
import { API_URL } from "./config";

export default function Login({onLogin}) {
  const [email,setEmail] = useState("");
  const [password,setPassword] = useState("");
  async function submit(e){
    e.preventDefault();
    const res = await fetch(`${API_URL}/users/login`, {
      method: "POST",
      headers: {"Content-Type":"application/json"},
      body: JSON.stringify({email,password})
    });
    const data = await res.json();
    if (data.access_token) {
      localStorage.setItem("token", data.access_token);
      localStorage.setItem("email", email);
      onLogin({email, token: data.access_token});
    } else {
      alert("Login failed");
    }
  }
  return (
    <form onSubmit={submit}>
      <input value={email} onChange={e=>setEmail(e.target.value)} placeholder="email"/>
      <input type="password" value={password} onChange={e=>setPassword(e.target.value)} placeholder="password"/>
      <button>Login</button>
    </form>
  );
}

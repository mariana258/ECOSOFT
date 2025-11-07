
import React from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Dashboard from "./pages/Dashboard"; // 👈 importa el Dashboard
import ProveedorPanel from "./pages/ProveedorPanel";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/dashboard" element={<Dashboard />} /> {/* 👈 agrega la ruta */}
         <Route path="/proveedor" element={<ProveedorPanel />} />
      </Routes>
    </BrowserRouter>
  );
}

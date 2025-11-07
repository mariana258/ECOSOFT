import React, { useState } from "react";

export default function ProveedorPanel() {
  const [seccionActiva, setSeccionActiva] = useState("usuarios");
  const [usuario] = useState({
    nombre: "Juan Pérez",
    rol: "Proveedor",
  });

  // Datos simulados (mock)
  const usuarios = [
    { id: 1, nombre: "María Gómez", correo: "maria@gmail.com", rol: "Cliente" },
    { id: 2, nombre: "Carlos López", correo: "carlos@gmail.com", rol: "Admin" },
  ];

  const pedidosPendientes = [
    { id: 1, cliente: "María Gómez", total: 50000, fecha: "2025-10-30" },
    { id: 2, cliente: "Carlos López", total: 72000, fecha: "2025-10-31" },
  ];

  const materialesActivos = [
    { id: 1, nombre: "Cartón", precio: 1500 },
    { id: 2, nombre: "Plástico", precio: 2000 },
  ];

  const materialesProveedor = [
    { id: 1, nombre: "Vidrio", precio: 2500 },
    { id: 2, nombre: "Papel", precio: 1000 },
  ];

  const facturas = [
    { id: 1, cliente: "María Gómez", fecha: "2025-10-28", archivo: "Factura_001.pdf" },
    { id: 2, cliente: "Carlos López", fecha: "2025-10-30", archivo: "Factura_002.pdf" },
  ];

  const handleDescargar = (nombre) => {
    alert(`Descargando ${nombre}...`);
  };

  const handleEditar = (tipo, id) => {
    alert(`Editando ${tipo} con ID: ${id}`);
  };

  const handleEliminar = (tipo, id) => {
    alert(`Eliminando ${tipo} con ID: ${id}`);
  };

  return (
    <div className="min-h-screen bg-emerald-50 text-gray-800">
      {/* Header */}
      <header className="bg-emerald-600 text-white flex justify-between items-center p-4 shadow-md">
        <div className="flex space-x-4">
          <button onClick={() => setSeccionActiva("usuarios")} className="hover:underline">Usuarios</button>
          <button onClick={() => setSeccionActiva("pedidos")} className="hover:underline">Pedidos</button>
          <button onClick={() => setSeccionActiva("materiales")} className="hover:underline">Materiales</button>
          <button onClick={() => setSeccionActiva("facturas")} className="hover:underline">Facturas</button>
        </div>
        <div className="flex items-center space-x-4">
          <span>{usuario.nombre} ({usuario.rol})</span>
          <button className="bg-white text-emerald-600 px-3 py-1 rounded hover:bg-emerald-100">Configuración</button>
          <button className="bg-red-500 px-3 py-1 rounded hover:bg-red-600 text-white">Cerrar sesión</button>
        </div>
      </header>

      {/* Contenido dinámico */}
      <main className="p-6 grid grid-cols-1 md:grid-cols-2 gap-6">
        {seccionActiva === "usuarios" && (
          <>
            {/* Caja 1 - Usuarios */}
            <div className="bg-white p-6 rounded-2xl shadow-md border border-emerald-100">
              <h2 className="text-xl font-bold text-emerald-700 mb-4">Usuarios registrados</h2>
              <ul>
                {usuarios.map((u) => (
                  <li key={u.id} className="flex justify-between items-center border-b py-2">
                    <span>{u.nombre} ({u.rol}) - {u.correo}</span>
                    <div className="space-x-2">
                      <button onClick={() => handleEditar("usuario", u.id)} className="text-blue-600 hover:underline">Editar</button>
                      <button onClick={() => handleEliminar("usuario", u.id)} className="text-red-600 hover:underline">Eliminar</button>
                    </div>
                  </li>
                ))}
              </ul>
            </div>

            {/* Caja 2 - Pedidos pendientes */}
            <div className="bg-white p-6 rounded-2xl shadow-md border border-emerald-100">
              <h2 className="text-xl font-bold text-emerald-700 mb-4">Pedidos pendientes</h2>
              {pedidosPendientes.map((p) => (
                <div key={p.id} className="flex justify-between items-center border-b py-2">
                  <span>{p.cliente} - ${p.total.toLocaleString()} - {p.fecha}</span>
                  <button onClick={() => handleDescargar(`Factura_${p.id}.pdf`)} className="text-emerald-600 hover:underline">Ver PDF</button>
                </div>
              ))}
            </div>

            {/* Caja 3 - Materiales activos */}
            <div className="bg-white p-6 rounded-2xl shadow-md border border-emerald-100">
              <h2 className="text-xl font-bold text-emerald-700 mb-4">Materiales activos</h2>
              {materialesActivos.map((m) => (
                <div key={m.id} className="flex justify-between items-center border-b py-2">
                  <span>{m.nombre} - ${m.precio.toLocaleString()}</span>
                  <button onClick={() => handleEditar("material", m.id)} className="text-blue-600 hover:underline">Editar</button>
                </div>
              ))}
            </div>

            {/* Caja 4 - Materiales proveedor */}
            <div className="bg-white p-6 rounded-2xl shadow-md border border-emerald-100">
              <h2 className="text-xl font-bold text-emerald-700 mb-4">Materiales proveedor</h2>
              {materialesProveedor.map((m) => (
                <div key={m.id} className="flex justify-between items-center border-b py-2">
                  <span>{m.nombre} - ${m.precio.toLocaleString()}</span>
                  <div className="space-x-2">
                    <button onClick={() => handleEditar("materialProveedor", m.id)} className="text-blue-600 hover:underline">Editar</button>
                    <button onClick={() => handleEliminar("materialProveedor", m.id)} className="text-red-600 hover:underline">Eliminar</button>
                  </div>
                </div>
              ))}
            </div>
          </>
        )}

        {seccionActiva === "facturas" && (
          <>
            {/* Caja 5 - Facturas PDF */}
            <div className="bg-white p-6 rounded-2xl shadow-md border border-emerald-100">
              <h2 className="text-xl font-bold text-emerald-700 mb-4">Facturas PDF</h2>
              {facturas.map((f) => (
                <div key={f.id} className="flex justify-between items-center border-b py-2">
                  <span>{f.cliente} - {f.fecha}</span>
                  <button onClick={() => handleDescargar(f.archivo)} className="text-emerald-600 hover:underline">Descargar</button>
                </div>
              ))}
            </div>

            {/* Caja 6 - Eliminar usuarios */}
            <div className="bg-white p-6 rounded-2xl shadow-md border border-emerald-100">
              <h2 className="text-xl font-bold text-emerald-700 mb-4">Eliminar o editar usuarios</h2>
              {usuarios.map((u) => (
                <div key={u.id} className="flex justify-between items-center border-b py-2">
                  <span>{u.nombre} - {u.correo}</span>
                  <div className="space-x-2">
                    <button onClick={() => handleEditar("usuario", u.id)} className="text-blue-600 hover:underline">Editar</button>
                    <button onClick={() => handleEliminar("usuario", u.id)} className="text-red-600 hover:underline">Eliminar</button>
                  </div>
                </div>
              ))}
            </div>
          </>
        )}
      </main>
    </div>
  );
}

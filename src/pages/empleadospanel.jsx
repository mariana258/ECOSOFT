import React, { useState, useEffect } from "react";
import { Menu, LogOut } from "lucide-react";

export default function EmployeeDashboard() {
  const [menuOpen, setMenuOpen] = useState(false);
  const [pedidos, setPedidos] = useState([]);
  const [filtro, setFiltro] = useState("pendiente");

  useEffect(() => {
    // Simulación de pedidos del backend
    const pedidosEjemplo = [
      { id: 1, cliente: "Carlos Pérez", material: "Vidrio", cantidad: 20, estado: "pendiente" },
      { id: 2, cliente: "Ana Gómez", material: "Plástico", cantidad: 15, estado: "en proceso" },
      { id: 3, cliente: "Laura Díaz", material: "Cartón", cantidad: 10, estado: "completado" },
    ];
    setPedidos(pedidosEjemplo);
  }, []);

  const actualizarEstado = (id, nuevoEstado) => {
    setPedidos((prev) =>
      prev.map((p) => (p.id === id ? { ...p, estado: nuevoEstado } : p))
    );
  };

  const pedidosFiltrados = pedidos.filter((p) =>
    filtro === "todos" ? true : p.estado === filtro
  );

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Navbar */}
      <header className="bg-green-700 text-white flex justify-between items-center p-4 shadow-md">
        <h1 className="text-2xl font-bold">Panel de Empleados</h1>
        <div className="flex items-center space-x-4">
          <button onClick={() => setMenuOpen(!menuOpen)} className="md:hidden">
            <Menu size={28} />
          </button>
          <button className="hidden md:flex items-center gap-2 bg-green-800 px-3 py-1 rounded-lg hover:bg-green-900">
            <LogOut size={18} />
            Cerrar Sesión
          </button>
        </div>
      </header>

      {/* Menú lateral */}
      <aside
        className={`fixed top-0 left-0 h-full w-64 bg-white shadow-lg p-4 transform transition-transform ${
          menuOpen ? "translate-x-0" : "-translate-x-full"
        } md:translate-x-0`}
      >
        <h2 className="text-lg font-semibold text-gray-700 mb-4">Menú</h2>
        <ul className="space-y-2">
          <li>
            <button
              className={`w-full text-left px-3 py-2 rounded-lg ${
                filtro === "pendiente"
                  ? "bg-green-700 text-white"
                  : "hover:bg-green-100"
              }`}
              onClick={() => setFiltro("pendiente")}
            >
              Pedidos Pendientes
            </button>
          </li>
          <li>
            <button
              className={`w-full text-left px-3 py-2 rounded-lg ${
                filtro === "en proceso"
                  ? "bg-green-700 text-white"
                  : "hover:bg-green-100"
              }`}
              onClick={() => setFiltro("en proceso")}
            >
              En Proceso
            </button>
          </li>
          <li>
            <button
              className={`w-full text-left px-3 py-2 rounded-lg ${
                filtro === "completado"
                  ? "bg-green-700 text-white"
                  : "hover:bg-green-100"
              }`}
              onClick={() => setFiltro("completado")}
            >
              Completados
            </button>
          </li>
          <li>
            <button
              className={`w-full text-left px-3 py-2 rounded-lg ${
                filtro === "todos"
                  ? "bg-green-700 text-white"
                  : "hover:bg-green-100"
              }`}
              onClick={() => setFiltro("todos")}
            >
              Todos los Pedidos
            </button>
          </li>
        </ul>
      </aside>

      {/* Contenido principal */}
      <main className="md:ml-64 p-6">
        <h2 className="text-2xl font-semibold mb-4 text-gray-800">
          {filtro === "todos"
            ? "Todos los pedidos"
            : `Pedidos ${filtro.charAt(0).toUpperCase() + filtro.slice(1)}`}
        </h2>

        <div className="overflow-x-auto bg-white rounded-lg shadow-md">
          <table className="min-w-full text-sm text-gray-700">
            <thead className="bg-green-700 text-white">
              <tr>
                <th className="py-2 px-4 text-left">ID</th>
                <th className="py-2 px-4 text-left">Cliente</th>
                <th className="py-2 px-4 text-left">Material</th>
                <th className="py-2 px-4 text-left">Cantidad</th>
                <th className="py-2 px-4 text-left">Estado</th>
                <th className="py-2 px-4 text-center">Acciones</th>
              </tr>
            </thead>
            <tbody>
              {pedidosFiltrados.map((pedido) => (
                <tr
                  key={pedido.id}
                  className="border-b hover:bg-gray-100 transition"
                >
                  <td className="py-2 px-4">{pedido.id}</td>
                  <td className="py-2 px-4">{pedido.cliente}</td>
                  <td className="py-2 px-4">{pedido.material}</td>
                  <td className="py-2 px-4">{pedido.cantidad}</td>
                  <td className="py-2 px-4 capitalize">{pedido.estado}</td>
                  <td className="py-2 px-4 text-center">
                    {pedido.estado !== "completado" && (
                      <div className="flex justify-center gap-2">
                        {pedido.estado === "pendiente" && (
                          <button
                            onClick={() =>
                              actualizarEstado(pedido.id, "en proceso")
                            }
                            className="bg-yellow-500 hover:bg-yellow-600 text-white px-3 py-1 rounded-lg"
                          >
                            Iniciar
                          </button>
                        )}
                        {pedido.estado === "en proceso" && (
                          <button
                            onClick={() =>
                              actualizarEstado(pedido.id, "completado")
                            }
                            className="bg-green-600 hover:bg-green-700 text-white px-3 py-1 rounded-lg"
                          >
                            Completar
                          </button>
                        )}
                      </div>
                    )}
                  </td>
                </tr>
              ))}
              {pedidosFiltrados.length === 0 && (
                <tr>
                  <td
                    colSpan="6"
                    className="text-center py-4 text-gray-500 italic"
                  >
                    No hay pedidos en esta categoría.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </main>
    </div>
  );
}

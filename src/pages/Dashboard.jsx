import React, { useState, useRef, useEffect } from "react";
import { FaUserCircle } from "react-icons/fa";

export default function Dashboard() {
  const [selectedMaterial, setSelectedMaterial] = useState("");
  const [selectedMixto, setSelectedMixto] = useState("");
  const [cantidad, setCantidad] = useState("");
  const [metodoPago, setMetodoPago] = useState("");
  const [precio, setPrecio] = useState(0);
  const [pedidos, setPedidos] = useState([]);
  const [queja, setQueja] = useState("");
  const [menuOpen, setMenuOpen] = useState(false);

  const inicioRef = useRef(null);
  const materialesRef = useRef(null);
  const pedidosRef = useRef(null);
  const contactoRef = useRef(null);
  const quejasRef = useRef(null);

  const materiales = [
    { nombre: "Plástico", precio: 2000 },
    { nombre: "Cartón", precio: 1500 },
    { nombre: "Vidrio", precio: 1000 },
    { nombre: "Metal", precio: 2500 },
    { nombre: "Papel", precio: 1200 },
  ];

  useEffect(() => {
    let total = 0;
    const material = materiales.find((m) => m.nombre === selectedMaterial);
    if (material && cantidad) {
      total = material.precio * cantidad;
    } else if (selectedMixto && cantidad) {
      const mixtos = {
        "Cartón y Plástico": 1800,
        "Vidrio y Metal": 2200,
        "Papel y Cartón": 1400,
      };
      total = mixtos[selectedMixto] * cantidad;
    }
    setPrecio(total);
  }, [selectedMaterial, selectedMixto, cantidad]);

  const scrollToSection = (ref) => {
    ref.current?.scrollIntoView({ behavior: "smooth" });
  };

  const handleProveedorClick = () => {
    alert("✅ Su solicitud para ser proveedor ha sido enviada correctamente.");
  };

  const handleConfirmarPedido = () => {
    if (!cantidad || (!selectedMaterial && !selectedMixto) || !metodoPago) {
      alert("⚠️ Por favor complete todos los campos antes de confirmar el pedido.");
      return;
    }

    const nuevoPedido = {
      id: pedidos.length + 1,
      material: selectedMaterial || selectedMixto,
      cantidad,
      total: precio,
      fecha: new Date().toLocaleDateString(),
      metodoPago,
    };

    setPedidos([...pedidos, nuevoPedido]);
    alert("✅ Su pedido ha sido realizado con éxito.");
    setSelectedMaterial("");
    setSelectedMixto("");
    setCantidad("");
    setMetodoPago("");
    setPrecio(0);
  };

  const handleEnviarQueja = () => {
    if (!queja.trim()) {
      alert("⚠️ Por favor escriba su queja o reclamo.");
      return;
    }
    alert("✅ Su queja o reclamo ha sido enviada.");
    setQueja("");
  };

  const handleDescargar = (pedido) => {
    const contenido = `
      🧾 COMPROBANTE DE PEDIDO ECOSOFT
      Fecha: ${pedido.fecha}
      Material: ${pedido.material}
      Cantidad: ${pedido.cantidad} kg
      Total: $${pedido.total.toLocaleString()}
      Método de Pago: ${pedido.metodoPago}
    `;
    const blob = new Blob([contenido], { type: "text/plain;charset=utf-8" });
    const enlace = document.createElement("a");
    enlace.href = URL.createObjectURL(blob);
    enlace.download = `Comprobante_Pedido_${pedido.id}.txt`;
    enlace.click();
  };

  const handleCerrarSesion = () => {
    alert("👋 Sesión cerrada correctamente.");
    window.location.reload();
  };

  return (
    <div className="w-full">
      {/* HEADER */}
      <header className="w-full">
        <div className="bg-white flex justify-between items-center px-8 py-4 shadow-md rounded-3xl">
          <h1 className="text-3xl font-extrabold text-green-700 tracking-wide">EC♻️SOFT</h1>

          <div className="relative flex items-center space-x-4">
            <button
              onClick={() => setMenuOpen(!menuOpen)}
              className="flex items-center gap-2 bg-emerald-600 text-white px-5 py-2 rounded-full font-semibold hover:bg-emerald-700 transition"
            >
              <FaUserCircle className="text-xl" />
              Cliente
            </button>

            {menuOpen && (
              <div className="absolute right-0 top-full mt-2 w-56 bg-white border border-gray-200 rounded-lg shadow-lg text-gray-700 z-50">
                <button
                  onClick={() => {
                    alert("✏️ Editar perfil");
                    setMenuOpen(false);
                  }}
                  className="block w-full text-left px-4 py-3 hover:bg-gray-100"
                >
                  ✏️ Editar perfil
                </button>
                <button
                  onClick={() => {
                    alert("⚙️ Configuración");
                    setMenuOpen(false);
                  }}
                  className="block w-full text-left px-4 py-3 hover:bg-gray-100"
                >
                  ⚙️ Configuración
                </button>
                <button
                  onClick={handleCerrarSesion}
                  className="block w-full text-left px-4 py-3 text-red-600 hover:bg-gray-100"
                >
                  🔒 Cerrar sesión
                </button>
              </div>
            )}
          </div>
        </div>
      </header>

      {/* NAV */}
      <nav className="bg-emerald-200 flex justify-center space-x-10 py-10 text-emerald-800 text-2xl font-medium">
        <button onClick={() => scrollToSection(inicioRef)} className="hover:text-green-500 transition">
          Inicio
        </button>
        <button onClick={() => scrollToSection(materialesRef)} className="hover:text-green-500 transition">
          Materiales
        </button>
        <button onClick={() => scrollToSection(pedidosRef)} className="hover:text-green-500 transition">
          Pedidos
        </button>
        <button onClick={() => scrollToSection(contactoRef)} className="hover:text-green-500 transition">
          Contacto
        </button>
        <button onClick={() => scrollToSection(quejasRef)} className="hover:text-green-500 transition">
          Quejas
        </button>
      </nav>

      {/* BIENVENIDA */} 
        <section ref={inicioRef} className=""></section>
<div  ref={inicioRef}className  ="flex items-center justify-center gap-20 bg-white-50 py-10 px-8 rounded-3xl shadow-sm">
  <div className="text-left text-emerald-900">
   
    <h2 className="text-5xl font-extrabold text-green-700 mb-6">
      BIENVENIDO A EC♻️SOFT
    </h2>
    <h3 ref={inicioRef} className="text-3xl font-poppins py-4 text-emerald-700 mb-2">Misión</h3>
    <p className="max-w-4xl text-4xl mb-4 ">
      Desarrollar soluciones tecnológicas sostenibles que optimicen los procesos de recolección y gestión de residuos, 
      promoviendo la eficiencia operativa de las empresas de reciclaje y contribuyendo al cuidado del medio ambiente. 
      A través de EcoSoft, buscamos integrar innovación, responsabilidad ecológica 
      y tecnología para impulsar una gestión inteligente y sostenible de los recursos.
    </p>
    <h3 className="text-3xl font-poppins py-4 text-emerald-700 mb-2">Visión</h3>
    <p className="max-w-4xl text-4xl  ">
      Ser la plataforma lider en Latinoamérica en gestión 
      digital para el sector del reciclaje, reconocida por su compromiso ambiental, 
      su innovación tecnológica y su aporte al desarrollo sostenible de las comunidades. Para 2030, Ecosoft aspira
      a convertirse en un referente en transformación digital verde.
    </p>
  </div>

  <img
    src="https://img.freepik.com/premium-photo/employees-recycling-industry-inspect-plastic-bottle-raw-materials-be-used-recycling-process_73899-19224.jpg"
    alt="reciclaje"
    className="w-100 h-100 rounded-2xl  object-contain mt-50"
  />
</div>

{/* SECCIÓN QUIERO SER PROVEEDOR */}
<section ref={inicioRef} className="flex justify-center mt-16 flex flex-col items-center">
  <div className="bg-emerald-100 p-10 rounded-3xl shadow-md border border-emerald-200 text-center w-[60%]">
    <h2 className="text-2xl font-semibold text-emerald-700 mb-4">
      ¿Eres una empresa o persona interesada en colaborar con nosotros?
    </h2>
    <p className="text-emerald-800 mb-6 text-1xl">
      Únete a nuestra red de proveedores y forma parte del cambio sostenible 🌎
    </p>
    <button
      onClick={handleProveedorClick}
      className="bg-emerald-600 text-white px-8 py-3 rounded-full font-semibold text-lg hover:bg-emerald-700 shadow-md transition"
    >
      Quiero ser proveedor
    </button>
  </div>
</section>
      
      

      {/* CONTENIDO PRINCIPAL */}
      <main className="max-w-[95%] mx-auto flex flex-col items-center px-10 py-12 space-y-16">
        {/* MATERIALES DISPONIBLES */}
        <section ref={materialesRef} className="bg-white/90 rounded-3xl p-10 shadow-lg border border-emerald-100 w-[85%]">
          <h2 className="text-3xl font-bold text-emerald-700 mb-8 text-center">
            Materiales Disponibles
          </h2>

          <div className="grid grid-cols-2 gap-10 text-center">
            <div className="bg-emerald-50 p-6 rounded-2xl shadow-md border border-emerald-200">
              <h3 className="text-2xl font-semibold text-emerald-700 mb-4">Material Individual</h3>
              <table className="w-full text-left border-collapse text-2lg">
                <thead>
                  <tr className="border-b-2 border-emerald-300 ">
                    <th className="p-4">Material</th>
                    <th className="p-4">Precio por kg</th>
                  </tr>
                </thead>
                <tbody>
                  {materiales.map((m, i) => (
                    <tr key={i} className="border-b border-emerald-200 hover:bg-emerald-100 transition">
                      <td className="p-4">{m.nombre}</td>
                      <td className="p-4">${m.precio.toLocaleString()}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            <div className="bg-emerald-50 p-6 rounded-2xl shadow-md border border-emerald-200">
              <h3 className="text-2xl font-semibold text-emerald-700 mb-4">Material Mixto</h3>
              <table className="w-full text-left border-collapse text-2lg">
                <thead>
                  <tr className="border-b-2 border-emerald-300">
                    <th className="p-4">Combinación</th>
                    <th className="p-4">Precio por kg</th>
                  </tr>
                </thead>
                <tbody>
                  <tr className="border-b border-emerald-200 hover:bg-emerald-100 transition">
                    <td className="p-4">Cartón y Plástico</td>
                    <td className="p-4">$1,800</td>
                  </tr>
                  <tr className="border-b border-emerald-200 hover:bg-emerald-100 transition">
                    <td className="p-4">Vidrio y Metal</td>
                    <td className="p-4">$2,200</td>
                  </tr>
                  <tr className="border-b border-emerald-200 hover:bg-emerald-100 transition">
                    <td className="p-4">Papel y Cartón</td>
                    <td className="p-4">$1,400</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </section>

        {/* REALIZAR PEDIDO */}
        <section ref={pedidosRef} className="bg-white-50 p-10 rounded-3xl shadow-md border border-emerald-200 text-center w-[85%]">
          <h2 className="text-3xl font-bold text-emerald-700 mb-8 text-center">Realizar Pedido</h2>

          <div className="grid grid-cols-2 gap-10 text-lg">
            <div>
              <label className="block font-semibold mb-3 text-center">Material Individual</label>
              <select
                value={selectedMaterial}
                onChange={(e) => {
                  setSelectedMaterial(e.target.value);
                  setSelectedMixto("");
                }}
                className="w-[80%] p-5 border rounded-2xl text-lg focus:ring-2 focus:ring-emerald-400"
              >
                <option value="">Seleccionar...</option>
                {materiales.map((m) => (
                  <option key={m.nombre} value={m.nombre}>
                    {m.nombre}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label className="block font-semibold mb-3 text-center">Material Mixto</label>
              <select
                value={selectedMixto}
                onChange={(e) => {
                  setSelectedMixto(e.target.value);
                  setSelectedMaterial("");
                }}
                className="w-[80%] p-5 border rounded-2xl text-lg focus:ring-2 focus:ring-emerald-400"
              >
                <option value="">Seleccionar...</option>
                <option value="Cartón y Plástico">Cartón y Plástico</option>
                <option value="Vidrio y Metal">Vidrio y Metal</option>
                <option value="Papel y Cartón">Papel y Cartón</option>
              </select>
            </div>

            <div>
              <label className="block font-semibold mb-3 text-center">Cantidad (KG)</label>
              <input
                type="number"
                
                value={cantidad}
                onChange={(e) => setCantidad(e.target.value)}
                className="w-[80%] p-5 border rounded-2xl bg-gray-200  text-lg focus:ring-2 focus:ring-emerald-400"
              />
            </div>

            <div>
              <label className="block font-semibold mb-3 text-center">Método de Pago</label>
              <select
                value={metodoPago}
                onChange={(e) => setMetodoPago(e.target.value)}
                className="w-[80%] p-5 border rounded-2xl text-lg focus:ring-2 focus:ring-emerald-400"
              >
                <option value="">Seleccionar...</option>
                <option value="Efectivo">Efectivo</option>
                <option value="Transferencia">Transferencia</option>
              </select>
            </div>

            <div className="col-span-2">
              <label className="block font-semibold mb-3 text-center">Total</label>
              <input
                type="text"
                value={`$${precio.toLocaleString()}`}
                readOnly
                className="w-[80%] p-5 border rounded-2xl text-lg bg-gray-200 text-center font-semibold"
              />
            </div>
          </div>

          <div className="flex justify-center mt-10">
            <button
              onClick={handleConfirmarPedido}
              className="bg-emerald-600 text-white px-10 py-4 rounded-2xl font-semibold text-lg hover:bg-emerald-700 shadow-md transition"
            >
              Confirmar Pedido
            </button>
          </div>

          {pedidos.length > 0 && (
            <div className="mt-12 w-[85%]">
              <h3 className="text-2xl font-bold text-emerald-700 mb-4 text-center">Pedidos Realizados</h3>
              <table className="w-full text-left border-collapse text-lg">
                <thead>
                  <tr className="border-b-2 border-emerald-300 text-center">
                    <th className="p-4">Fecha</th>
                    <th className="p-4">Material</th>
                    <th className="p-4">Cantidad (kg)</th>
                    <th className="p-4">Total</th>
                    <th className="p-4">Comprobante</th>
                  </tr>
                </thead>
                <tbody>
                  {pedidos.map((p) => (
                    <tr key={p.id} className="border-b border-emerald-200 text-center hover:bg-emerald-50">
                      <td className="p-4">{p.fecha}</td>
                      <td className="p-4">{p.material}</td>
                      <td className="p-4">{p.cantidad}</td>
                      <td className="p-4">${p.total.toLocaleString()}</td>
                      <td className="p-4">
                        <button
                          onClick={() => handleDescargar(p)}
                          className="bg-emerald-500 text-white px-5 py-2 rounded-xl hover:bg-emerald-600 transition"
                        >
                          Descargar
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </section>

        {/* CONTACTO */}
        <section
          ref={contactoRef}
          className="bg-white/90 rounded-3xl p-10 shadow-lg border border-emerald-100 flex justify-between items-center w-[85%] "
        >
          <div className="text-lg text-emerald-800 space-y-3 w-1/2 pl-10 ">
            <h2 className="text-3xl font-bold text-emerald-700 mb-6 text-left">Contacto</h2>
            <p>
              <strong>Dirección:</strong> Calle 45 #22-18, Bogotá, Colombia
            </p>
            <p>
              <strong>Teléfono:</strong> +57 320 456 7890
            </p>
            <p>
              <strong>Correo:</strong> ecosoft.emp@gmail.com
            </p>
          </div>
          <div className="w-1/2 pr-10">
            <iframe
              title="Ubicación ECOSOFT"
              src="https://maps.app.goo.gl/uyhG2kuXaCzoaSJ37"
              width="100%"
              height="300"
              allowFullScreen=""
              loading="lazy"
              className="rounded-2xl border border-emerald-200 shadow-md"
            ></iframe>
          </div>
        </section>

        {/* QUEJAS O RECLAMOS */}
        <section
          ref={quejasRef}
          className="bg-white/90 rounded-3xl p-10 shadow-lg border border-emerald-100 flex items-center justify-between w-[85%]"
        >
          <div className="w-2/3">
            <h2 className="text-3xl font-bold text-emerald-700 mb-8 text-left">Quejas o Reclamos</h2>
            <textarea
              value={queja}
              onChange={(e) => setQueja(e.target.value)}
              placeholder="Describe tu queja o reclamo..."
              className="w-3/4 p-4 rounded-2xl border text-lg focus:ring-2 focus:ring-emerald-400"
              rows="3"
            ></textarea>

            <div className="mt-4">
              <button
                onClick={handleEnviarQueja}
                className="bg-emerald-600 text-white px-8 py-3 rounded-2xl font-semibold text-lg hover:bg-emerald-700 shadow-md transition"
              >
                Enviar
              </button>
            </div>
          </div>

          <div className="w-1/3 flex flex-col items-center">
            <p className="text-emerald-800 text-lg font-medium mb-4 text-center">
              
            </p>
          
             
            
          </div>
        </section>
      </main>

      {/* FOOTER */}
      <footer className="bg-emerald-700  rounded-3xl text-white text-center py-10 mt-20 shadow-inner text-lg">
        <p>© 2025 ECOSOFT — Todos los derechos reservados.</p>
        <p className="mt-2 text-emerald-200">Comprometidos con el medio ambiente 🌱</p>
      </footer>
    </div>
  );
}

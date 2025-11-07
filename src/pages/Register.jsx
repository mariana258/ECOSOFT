import React from "react";
import { useNavigate } from "react-router-dom";

export default function Register() {
  const navigate = useNavigate();

  const handleSubmit = (e) => {
    e.preventDefault();
    navigate("/dashboard");
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-emerald-100 via-emerald-100 to-emerald-300 relative overflow-hidden">
      {/* Fondo decorativo opcional */}
      <div className="absolute inset-0 bg-[url('/img/eco-pattern.png')] opacity-10 bg-cover bg-center"></div>

      {/* Contenedor principal */}
      <div className="relative z-10 bg-white/95 backdrop-blur-md rounded-3xl shadow-2xl p-14 w-full max-w-6xl text-emerald-800">
        <h1 className="text-4xl font-extrabold text-center mb-3 text-emerald-700 tracking-wide">
          ECOSOFT
        </h1>
        <h2 className="text-2xl font-semibold text-center mb-8">
          Crear Cuenta
        </h2>

        <form onSubmit={handleSubmit} className="flex flex-col space-y-16">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            <div>
              <label className="block text-lg font-semibold mb-2 ">
                Nombre completo
              </label>
              <input
                type="text"
                placeholder="Tu nombre completo"
                className="w-full p-4 rounded-2xl border border-emerald-300 focus:outline-none focus:ring-4 focus:ring-emerald-400 transition"
                required
              />
            </div>
            <div>
              <label className="block text-lg font-semibold mb-2">
                Correo electrónico
              </label>
              <input
                type="email"
                placeholder="ejemplo@correo.com"
                className="w-full p-4 rounded-2xl border border-emerald-300 focus:outline-none focus:ring-4 focus:ring-emerald-400 transition"
                required
              />
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            <div>
              <label className="block text-lg font-semibold mb-2">
                Contraseña
              </label>
              <input
                type="password"
                placeholder="Crea una contraseña"
                className="w-full p-4 rounded-2xl border border-emerald-300 focus:outline-none focus:ring-4 focus:ring-emerald-400 transition"
                required
              />
            </div>
            <div>
              <label className="block text-lg font-semibold mb-2">
                Teléfono
              </label>
              <input
                type="tel"
                placeholder="+57 300 000 0000"
                className="w-full p-4 rounded-2xl border border-emerald-300 focus:outline-none focus:ring-4 focus:ring-emerald-400 transition"
                required
              />
            </div>
          </div>

          <button
            type="submit"
            className="w-full py-4 bg-emerald-600 text-white font-semibold rounded-2xl hover:bg-emerald-700 shadow-md hover:shadow-lg transition-all duration-300 text-lg"
          >
            Registrarme
          </button>
        </form>

        <p className="text-center text-lg mt-10 text-emerald-700">
          ¿Ya tienes una cuenta?{" "}
          <button
            onClick={() => navigate("/login")}
            className="text-emerald-600 font-semibold hover:underline"
          >
            Inicia sesión aquí
          </button>
        </p>
      </div>
    </div>
  );
}

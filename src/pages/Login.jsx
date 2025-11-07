import React from "react";
import { useNavigate } from "react-router-dom";
import { ArrowLeft } from "lucide-react"; // 👈 Asegúrate de tener lucide-react instalado

export default function Login() {
  const navigate = useNavigate();

  const handleSubmit = (e) => {
    e.preventDefault();
    navigate("/dashboard");
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-emerald-200 via-emerald-100 to-emerald-600 relative overflow-hidden">
      {/* Fondo decorativo */}
      <div className="absolute inset-0 bg-[url('/img/eco-pattern.png')] opacity-10 bg-cover bg-center"></div>

      {/* 🔙 Botón Volver */}
      <button
        onClick={() => navigate("/")}
        className="absolute top-6 left-6 flex items-center gap-2 text-emerald-800 bg-white/90 hover:bg-white px-4 py-2 rounded-full shadow-md transition-all duration-300 font-semibold"
      >
        <ArrowLeft size={30} />
        Volver
      </button>

      {/* Contenedor principal */}
       <div className=" bg-[url('https://img.freepik.com/free-photo/eco-friendly-recycling-concept_23-2148857335.jpg')] bg-cover bg-center"></div>
      <div className="relative z-10 bg-white/95 backdrop-blur-md rounded-3xl shadow-2xl p-14 w-full max-w-4xl text-emerald-800">


       
        <h1 className="text-4xl font-extrabold text-center mb-3 text-emerald-700 tracking-wide">
          ECOSOFT
        </h1>
        <h2 className="text-2xl font-semibold text-center mb-8">
          Iniciar Sesión
        </h2>

        <form onSubmit={handleSubmit} className="flex flex-col space-y-16">
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

          <div>
            <label className="block text-lg font-semibold mb-2">
              Contraseña
            </label>
            <input
              type="password"
              placeholder="••••••••"
              className="w-full p-4 rounded-2xl border border-emerald-300 focus:outline-none focus:ring-4 focus:ring-emerald-400 transition"
              required
            />
          </div>

          <div className="flex justify-between items-center text-sm">
            <button
              type="button"
              onClick={() =>
                alert("Función para recuperar contraseña próximamente.")
              }
              className="text-emerald-600 font-semibold hover:underline text-lg"
            >
              ¿Olvidaste tu contraseña?
            </button>
          </div>

          <button
            type="submit"
            className="w-full py-4 bg-emerald-600 text-white font-semibold rounded-2xl hover:bg-emerald-700 shadow-md hover:shadow-lg transition-all duration-300 text-lg"
          >
            Ingresar
          </button>
        </form>

        <p className="text-center text-lg mt-10 text-emerald-700">
          ¿No tienes cuenta?{" "}
          <button
            onClick={() => navigate("/register")}
            className="text-emerald-600 font-semibold hover:underline"
          >
            Regístrate aquí
          </button>
        </p>
      </div>
    </div>
  );
}

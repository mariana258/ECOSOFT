import React from "react";

export default function Home() {
  return (
    <div className="min-h-screen flex flex-col bg-emerald-50">
      {/* HEADER */}
      <header className="bg-white shadow-sm sticky top-0 z-50">
        <div className="max-w-7xl mx-auto flex items-center justify-between p-4">
          <h1 className="text-2xl font-extrabold text-emerald-800 flex items-center gap-2">
            ♻️ ECOSOFT
          </h1>
          <div className="space-x-4">
            <a
              href="/register"
              className="border border-emerald-600 text-emerald-700 px-4 py-2 rounded-md hover:bg-emerald-50 transition"
            >
              Regístrate
            </a>
            <a
              href="/login"
              className="bg-emerald-700 text-white px-4 py-2 rounded-md hover:bg-emerald-800 transition"
            >
              Iniciar sesión
            </a>
          </div>
        </div>
      </header>

      {/* HERO SECTION */}
      <section className="bg-gradient-to-r from-emerald-700 to-emerald-300 text-white py-20">
        <div className="max-w-7xl mx-auto flex flex-col md:flex-row items-center justify-between px-6">
          <div className="md:w-1/2 space-y-4">
            <h2 className="text-5xl font-extrabold leading-tight">
              BIENVENIDOS A <br /> EC♻️SOFT
            </h2>
          </div>
          <div className="md:w-1/2 mt-8 md:mt-0">
            <p className="text-3xl leading-base">
              Somos una empresa enfocada en optimizar la recolección, el uso de
              recursos y el control de insumos, generando beneficios para
              empresas y el medio ambiente.
            </p>
          </div>
        </div>
      </section>

      {/* MATERIALES */}
      <section className="max-w-7xl mx-auto py-20 px-6">
        <h3 className="text-4xl font-bold text-center text-emerald-800 mb-12">
          Nuestros materiales
        </h3>
        <div className="grid md:grid-cols-3 gap-8">
          {/* Cartón */}
          <div className="bg-white shadow-lg rounded-2xl overflow-hidden hover:shadow-2xl transition">
            <img
              src="https://www.cajacartonembalaje.com/blog/wp-content/uploads/2017/03/shutterstock_99009155-300x199.jpg"
              alt="Cartón"
              className="w-full h-56 object-cover"
            />
            <div className="p-6">
              <h4 className="text-xl font-semibold text-emerald-700">Cartón</h4>
              <p className="text-gray-600 text-xl">Reciclaje de cartón y cajas</p>
            </div>
          </div>

          {/* Plástico */}
          <div className="bg-white shadow-lg rounded-2xl overflow-hidden hover:shadow-2xl transition">
            <img
              src="data:image/jpeg;base64,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"
              alt="Plástico"
              className="w-full h-56 object-cover"
            />
            <div className="p-6">
              <h4 className="text-xl font-semibold text-emerald-700">
                Plástico
              </h4>
              <p className="text-gray-600 text-xl">Gestión de plásticos reciclables</p>
            </div>
          </div>

          {/* Papel */}
          <div className="bg-white shadow-lg rounded-2xl overflow-hidden hover:shadow-2xl transition">
            <img
              src="https://www.stampaprint.net/es/blog/wp-content/uploads/2016/05/diferencias-papel-ecologico-y-reciclado-1.jpg"
              alt="Papel"
              className="w-full h-56 object-cover"
            />
            <div className="p-6">
              <h4 className="text-xl font-semibold text-emerald-700">Papel</h4>
              <p className="text-gray-600 text-xl">Recolección de papel usado</p>
            </div>
          </div>
        </div>
      </section>

      {/* BENEFICIOS */}
      <section className="bg-emerald-100 py-20 px-6">
        <div className="max-w-7xl mx-auto text-center">
          <h3 className="text-4xl font-bold text-emerald-800 mb-12">
            Beneficios de trabajar con nosotros
          </h3>
          <div className="grid md:grid-cols-3 gap-8">
            <div className="bg-white shadow-md rounded-xl p-8 hover:shadow-2xl transition">
              <h4 className="text-xl font-semibold text-emerald-700 mb-3">
                🌱 Impacto Ambiental Positivo
              </h4>
              <p className="text-gray-600 text-xl">
                Contribuye al cuidado del planeta reduciendo desechos y
                promoviendo prácticas sostenibles.
              </p>
            </div>
            <div className="bg-white shadow-md rounded-xl p-8 hover:shadow-2xl transition">
              <h4 className="text-xl font-semibold text-emerald-700 mb-3">
                💼 Ahorro para tu Empresa
              </h4>
              <p className="text-gray-600 text-xl">
                Optimizamos recursos y reducimos costos en el manejo de residuos
                e insumos.
              </p>
            </div>
            <div className="bg-white shadow-md rounded-xl p-8 hover:shadow-2xl transition">
              <h4 className="text-xl font-semibold text-emerald-700 mb-3">
                🤝 Compromiso y Transparencia
              </h4>
              <p className="text-gray-600 text-xl">
                Brindamos acompañamiento constante con procesos claros y
                responsables.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* FOOTER */}
      <footer className="bg-white border-t border-gray-200 mt-16">
        <div className="max-w-7xl mx-auto py-10 px-6 grid md:grid-cols-4 gap-8 text-sm text-gray-700">
          <div>
            <h5 className="font-bold text-emerald-800 mb-3">♻️ ECOSOFT</h5>
            <p>
              Optimizando recursos y cuidando el medio ambiente para un futuro
              sostenible. 
            </p>
          </div>
          <div>
            <h5 className="font-semibold text-emerald-700 mb-3">Servicios</h5>
            <ul className="space-y-2 ">
              <li>Recolección de Cartón</li>
              <li>Gestión de Plásticos</li>
              <li>Reciclaje de Papel</li>
            </ul>
          </div>
          <div>
            <h5 className="font-semibold text-emerald-700 mb-3">Empresa</h5>
            <ul className="space-y-2">
              <li>Sobre Nosotros</li>
              <li>Nuestro Equipo</li>
              <li>Terminos y</li>
            </ul>
          </div>
          <div>
            <h5 className="font-semibold text-emerald-700 mb-3">Contacto</h5>
            <ul className="space-y-2">
              <li>📍 Av. Principal 123, Ciudad</li>
              <li>📞 +57 310 456 7890</li>
              <li>📧 Ecosoft.emp@gmail.com</li>
            </ul>
          </div>
        </div>
        <div className="bg-emerald-900 text-center text-white text-xs py-4">
          © {new Date().getFullYear()} EcoSoft — Todos los derechos reservados.
        </div>
      </footer>
    </div>
  );
}

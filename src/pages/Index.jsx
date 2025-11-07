import React from 'react';
import { Link } from 'react-router-dom';

export default function IndexPage(){
  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-r from-green-100 to-white">
      <div className="max-w-4xl p-8 bg-white rounded-2xl shadow-xl">
        <h1 className="text-4xl font-bold text-green-700 mb-4">Ecosoft </h1>
        <p className="mb-6">Somos una empresa dedicada a la gestión y reciclaje sostenible. Nuestra misión es transformar residuos en recursos, tecnologías pensadas para tecnólogos y equipos técnicos.</p>
        <div className="flex gap-4">
          <Link to="/register" className="px-4 py-2 bg-green-600 text-white rounded">Registrarse</Link>
          <Link to="/login" className="px-4 py-2 border border-green-600 text-green-600 rounded">Iniciar sesión</Link>
        </div>
      </div>
    </div>
  )
}
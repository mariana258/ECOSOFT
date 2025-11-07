import React from 'react';


export default function Footer() {
return (
<footer className="bg-green-700 text-white py-6 mt-auto">
<div className="max-w-6xl mx-auto px-4 flex flex-col md:flex-row justify-between items-center">
<p className="text-sm">© 2025 EcoSoft. Todos los derechos reservados.</p>
<div className="flex gap-4 mt-3 md:mt-0">
<a href="#" className="hover:text-green-300">Política de Privacidad</a>
<a href="#" className="hover:text-green-300">Términos de Uso</a>
</div>
</div>
</footer>
);
}
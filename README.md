# Ecosoft backend (local development)

Breve guía para ejecutar y probar el backend `Ecosoft` en desarrollo.

## Qué contiene
- `backend/` - código FastAPI (models, routes, schemas, core).
- `ecosoft.sql` - script SQL con DDL, triggers y datos iniciales (roles).
- `tests/` - pruebas pytest para validación de schemas.

## Requisitos
- Python 3.9+
- MySQL server (opcional para desarrollo; puedes ejecutar sólo pruebas sin BD)

## Instalación (PowerShell)
1. Instalar dependencias
```powershell
cd "C:\Users\ainel\OneDrive\Desktop\ecosoft\backend"
python -m pip install -r requirements.txt
python -m pip install -r "..\requirements-dev.txt"
```

2. Crear la base de datos (opcional, recommended to fully run the app)
 - Ejecuta el archivo `ecosoft.sql` en tu servidor MySQL (por ejemplo con MySQL Workbench o `mysql` CLI).

3. Variables de entorno
 - Crea un `.env` en `backend/` con las variables: MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_DB, MYSQL_PORT, SECRET_KEY, etc.

4. Ejecutar la aplicación
```powershell
cd "C:\Users\ainel\OneDrive\Desktop\ecosoft\backend"
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

## Probar (sin BD)
 - Puedes ejecutar las pruebas unitarias de schemas sin una base de datos:
```powershell
cd "C:\Users\ainel\OneDrive\Desktop\ecosoft"
pytest -q
```

## Cambios importantes realizados
- Mapeo de la columna `contraseña` (DB) a atributo Python `contrasena` para evitar caracteres no-ASCII en atributos.
- Añadido `HistorialInventario` y registro desde el backend cuando se ajusta stock.
- Alineación de `precio_compra` / `precio_venta` en schemas y rutas.
- Correcciones en importaciones de `models` (uso del paquete `models` en vez de importaciones de módulos no existentes).

Si quieres que arranque el servidor y ejecute pruebas de endpoints, necesito que Python esté disponible en tu entorno (o puedo guiarte para instalarlo). También puedo generar un script para aplicar `ecosoft.sql` automáticamente a una instancia MySQL si lo deseas.

# Sistema de Autenticación y CRUD - Ecosoft API

## 🔐 Autenticación JWT

### Endpoints de Autenticación

#### 1. Login
```http
POST /auth/login
Content-Type: application/x-www-form-urlencoded

username=user@example.com&password=micontraseña
```

**Respuesta:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer"
}
```

#### 2. Refresh Token
```http
POST /auth/refresh
Content-Type: application/json

{
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

#### 3. Obtener Usuario Actual
```http
GET /auth/me
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

## 📝 CRUDs Completos

### Usuarios
- ✅ `POST /usuarios/` - Registrar usuario
- ✅ `GET /usuarios/` - Listar usuarios
- ✅ `GET /usuarios/{id}` - Obtener usuario por ID
- ✅ `PUT /usuarios/{id}` - Actualizar usuario (requiere autenticación)
- ✅ `DELETE /usuarios/{id}` - Eliminar usuario (solo admin)
- ✅ `POST /usuarios/cambiar-contrasena` - Cambiar contraseña (requiere autenticación)
- ✅ `POST /usuarios/solicitar-rol/{rol_id}` - Solicitar rol
- ✅ `GET /usuarios/solicitudes` - Listar solicitudes de rol
- ✅ `PUT /usuarios/aprobar-solicitud/{id}` - Aprobar/rechazar solicitud

### Pedidos
- ✅ `POST /pedidos/` - Crear pedido
- ✅ `GET /pedidos/` - Listar pedidos
- ✅ `GET /pedidos/{id}` - Obtener pedido por ID
- ✅ `PUT /pedidos/{id}` - Actualizar pedido
- ✅ `DELETE /pedidos/{id}` - Eliminar pedido

### Pagos
- ✅ `POST /pagos/` - Crear pago
- ✅ `GET /pagos/` - Listar pagos
- ✅ `GET /pagos/{id}` - Obtener pago por ID
- ✅ `PUT /pagos/{id}` - Actualizar pago
- ✅ `DELETE /pagos/{id}` - Eliminar pago

### Facturas
- ✅ `POST /facturas/` - Crear factura
- ✅ `GET /facturas/` - Listar facturas
- ✅ `GET /facturas/{id}` - Obtener factura por ID
- ✅ `PUT /facturas/{id}` - Actualizar factura
- ✅ `DELETE /facturas/{id}` - Eliminar factura

### Materiales
- ✅ `POST /materiales/` - Crear material
- ✅ `GET /materiales/` - Listar materiales
- ✅ `GET /materiales/{id}` - Obtener material por ID
- ✅ `PUT /materiales/{id}` - Actualizar material
- ✅ `DELETE /materiales/{id}` - Eliminar material

### Inventario
- ✅ `GET /inventario/` - Listar inventario
- ✅ `GET /inventario/{id_material}` - Obtener inventario por material
- ✅ `GET /inventario/historial/{id_material}` - Ver historial
- ✅ `POST /inventario/ajustar` - Ajustar inventario

### Roles
- ✅ `POST /roles/` - Crear rol
- ✅ `GET /roles/` - Listar roles

## 🔒 Protección de Endpoints

### Uso Básico con Autenticación
```python
from core.security import get_current_user

@router.get('/protected')
def protected_endpoint(current_user: Usuario = Depends(get_current_user)):
    return {"message": f"Hola {current_user.nombre}"}
```

### Protección por Roles
```python
from core.security import require_roles

@router.delete('/admin-only')
def admin_endpoint(current_user: Usuario = Depends(require_roles(['administrador']))):
    return {"message": "Solo administradores"}
```

### Múltiples Roles Permitidos
```python
@router.post('/vendor-or-admin')
def vendor_endpoint(
    current_user: Usuario = Depends(require_roles(['administrador', 'vendedor']))
):
    return {"message": "Acceso permitido"}
```

## 🚀 Instalación

1. **Instalar dependencias:**
```bash
pip install -r backend/requirements.txt
```

2. **Configurar variables de entorno:**
```bash
cp .env.example .env
# Editar .env con tus configuraciones
```

3. **Ejecutar el servidor:**
```bash
cd backend
uvicorn main:app --reload
```

## 📚 Documentación Interactiva

Una vez el servidor esté corriendo:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔑 Ejemplo de Uso con JavaScript/Frontend

```javascript
// Login
const login = async (email, password) => {
  const formData = new URLSearchParams();
  formData.append('username', email);
  formData.append('password', password);
  
  const response = await fetch('http://localhost:8000/auth/login', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: formData
  });
  
  const data = await response.json();
  // Guardar tokens
  localStorage.setItem('access_token', data.access_token);
  localStorage.setItem('refresh_token', data.refresh_token);
};

// Hacer petición autenticada
const getUsers = async () => {
  const token = localStorage.getItem('access_token');
  
  const response = await fetch('http://localhost:8000/usuarios/', {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });
  
  return await response.json();
};
```

## 📋 Próximos Pasos Sugeridos

1. ✅ Conectar con la base de datos MySQL
2. ⬜ Añadir paginación a los endpoints de listado
3. ⬜ Implementar filtros y búsqueda
4. ⬜ Añadir validaciones de negocio más robustas
5. ⬜ Implementar logging y auditoría
6. ⬜ Crear tests de integración
7. ⬜ Añadir endpoints de estadísticas/métricas

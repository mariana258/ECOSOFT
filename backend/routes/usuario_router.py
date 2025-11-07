from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.database import get_db
from core.security import hash_password, verify_password, get_current_user, require_roles
from core.redis_client import get_from_cache, save_to_cache, delete_from_cache
from models import Usuario, Rol
from schemas.usuario_schema import UsuarioCreate, UsuarioResponse, UsuarioUpdate
from schemas.auth_schema import ChangePasswordRequest
from typing import List
router = APIRouter()
@router.post('/', response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
def registrar_usuario(payload: UsuarioCreate, db: Session = Depends(get_db)):
    if db.query(Usuario).filter(Usuario.email == payload.email).first():
        raise HTTPException(status_code=400, detail='Correo ya registrado')
    try:
        # map payload.contrasena to model attribute contrasena (column name in DB is `contraseña`)
        u = Usuario(nombre=payload.nombre, email=payload.email, telefono=payload.telefono, contrasena=hash_password(payload.contrasena), solicitud_rol='ninguna', rol_solicitado=None)
        db.add(u); db.commit(); db.refresh(u)
        rol_cliente = db.query(Rol).filter(Rol.nombre.ilike('cliente')).first()
        if rol_cliente:
            u.roles.append(rol_cliente)
            db.commit(); db.refresh(u)
        delete_from_cache('usuarios:list')
        return u
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.post('/solicitar-rol/{rol_id}')
def solicitar_rol(
    rol_id: int, 
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Solicitar un nuevo rol (el usuario debe estar autenticado)"""
    rol = db.query(Rol).filter(Rol.id_rol == rol_id).first()
    if not rol:
        raise HTTPException(status_code=404, detail='Rol no encontrado')
    if any(r.id_rol == rol_id for r in current_user.roles):
        raise HTTPException(status_code=400, detail='Usuario ya tiene ese rol')
    try:
        current_user.solicitud_rol = 'pendiente'
        current_user.rol_solicitado = rol_id
        db.commit()
        db.refresh(current_user)
        delete_from_cache('usuarios:list')
        return {'detail':'Solicitud creada', 'usuario_id': current_user.id_usuario, 'rol_solicitado': rol_id}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get('/solicitudes', response_model=list[UsuarioResponse])
def listar_solicitudes(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_roles(['administrador']))
):
    """Listar solicitudes de rol pendientes (solo administradores)"""
    usuarios = db.query(Usuario).filter(Usuario.solicitud_rol == 'pendiente').all()
    data = []
    for u in usuarios:
        data.append({'id_usuario': u.id_usuario, 'nombre': u.nombre, 'email': u.email, 'telefono': u.telefono, 'roles': [{'id_rol': r.id_rol, 'nombre': r.nombre} for r in u.roles], 'solicitud_rol': u.solicitud_rol, 'rol_solicitado': u.rol_solicitado, 'estado': u.estado, 'fecha_registro': u.fecha_registro.isoformat() if u.fecha_registro else None})
    return data

@router.put('/aprobar-solicitud/{usuario_id}')
def aprobar_solicitud(
    usuario_id: int, 
    aprobado: bool, 
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_roles(['administrador']))
):
    """Aprobar o rechazar solicitud de rol (solo administradores)"""
    u = db.query(Usuario).filter(Usuario.id_usuario == usuario_id).first()
    if not u or u.solicitud_rol != 'pendiente':
        raise HTTPException(status_code=404, detail='Solicitud no encontrada')
    if aprobado:
        rol = db.query(Rol).filter(Rol.id_rol == u.rol_solicitado).first()
        if not rol:
            raise HTTPException(status_code=404, detail='Rol no encontrado')
        try:
            u.roles.append(rol)
            u.solicitud_rol = 'aprobada'
            u.rol_solicitado = None
            db.commit(); db.refresh(u)
            delete_from_cache('usuarios:list')
            return {'detail':'Solicitud aprobada'}
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=str(e))
    else:
        try:
            u.solicitud_rol = 'rechazada'
            u.rol_solicitado = None
            db.commit(); db.refresh(u)
            delete_from_cache('usuarios:list')
            return {'detail':'Solicitud rechazada'}
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=str(e))
@router.get('/', response_model=list[UsuarioResponse])
def listar_usuarios(db: Session = Depends(get_db)):
    cached = get_from_cache('usuarios:list')
    if cached:
        return cached
    usuarios = db.query(Usuario).all()
    data = []
    for u in usuarios:
        data.append({'id_usuario': u.id_usuario, 'nombre': u.nombre, 'email': u.email, 'telefono': u.telefono, 'roles': [{'id_rol': r.id_rol, 'nombre': r.nombre, 'descripcion': r.descripcion} for r in u.roles], 'solicitud_rol': u.solicitud_rol, 'rol_solicitado': u.rol_solicitado, 'estado': u.estado, 'fecha_registro': u.fecha_registro.isoformat() if u.fecha_registro else None})
    save_to_cache('usuarios:list', data, ttl=300)
    return data

@router.get('/{id_usuario}', response_model=UsuarioResponse)
def obtener_usuario(id_usuario: int, db: Session = Depends(get_db)):
    """Obtener un usuario por ID"""
    usuario = db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()
    if not usuario:
        raise HTTPException(status_code=404, detail='Usuario no encontrado')
    return usuario

@router.put('/{id_usuario}', response_model=UsuarioResponse)
def actualizar_usuario(
    id_usuario: int, 
    payload: UsuarioUpdate, 
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Actualizar datos de un usuario (solo admins o el mismo usuario)"""
    usuario = db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()
    if not usuario:
        raise HTTPException(status_code=404, detail='Usuario no encontrado')
    
    # Verificar permisos: solo el mismo usuario o un admin
    user_roles = [rol.nombre.lower() for rol in current_user.roles]
    if current_user.id_usuario != id_usuario and 'administrador' not in user_roles:
        raise HTTPException(status_code=403, detail='No tienes permisos para actualizar este usuario')
    
    try:
        if payload.nombre is not None:
            usuario.nombre = payload.nombre
        if payload.email is not None:
            # Verificar que el email no esté en uso por otro usuario
            existing = db.query(Usuario).filter(
                Usuario.email == payload.email, 
                Usuario.id_usuario != id_usuario
            ).first()
            if existing:
                raise HTTPException(status_code=400, detail='Email ya está en uso')
            usuario.email = payload.email
        if payload.telefono is not None:
            usuario.telefono = payload.telefono
        if payload.estado is not None and 'administrador' in user_roles:
            # Solo admins pueden cambiar el estado
            usuario.estado = payload.estado
        
        db.commit()
        db.refresh(usuario)
        delete_from_cache('usuarios:list')
        return usuario
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.delete('/{id_usuario}', status_code=status.HTTP_204_NO_CONTENT)
def eliminar_usuario(
    id_usuario: int, 
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_roles(['administrador']))
):
    """Eliminar un usuario (solo administradores)"""
    usuario = db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()
    if not usuario:
        raise HTTPException(status_code=404, detail='Usuario no encontrado')
    
    if usuario.id_usuario == current_user.id_usuario:
        raise HTTPException(status_code=400, detail='No puedes eliminarte a ti mismo')
    
    try:
        db.delete(usuario)
        db.commit()
        delete_from_cache('usuarios:list')
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.post('/cambiar-contrasena', status_code=status.HTTP_200_OK)
def cambiar_contrasena(
    payload: ChangePasswordRequest,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Cambiar contraseña del usuario autenticado"""
    if not verify_password(payload.current_password, current_user.contrasena):
        raise HTTPException(status_code=400, detail='Contraseña actual incorrecta')
    
    if len(payload.new_password) < 6:
        raise HTTPException(status_code=400, detail='La nueva contraseña debe tener al menos 6 caracteres')
    
    try:
        current_user.contrasena = hash_password(payload.new_password)
        db.commit()
        return {'detail': 'Contraseña actualizada exitosamente'}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

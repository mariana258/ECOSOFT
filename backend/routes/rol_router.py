from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import get_db
from core.security import require_roles
from models import Rol, Usuario
from schemas.rol_schema import RolResponse, RolBase
router = APIRouter()

@router.post('/', response_model=RolResponse)
def crear_rol(
    payload: RolBase, 
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_roles(['administrador']))
):
    if db.query(Rol).filter(Rol.nombre == payload.nombre).first():
        raise HTTPException(status_code=400, detail='Rol ya existe')
    try:
        rol = Rol(nombre=payload.nombre, descripcion=payload.descripcion)
        db.add(rol)
        db.commit()
        db.refresh(rol)
        return rol
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get('/', response_model=list[RolResponse])
def listar_roles(db: Session = Depends(get_db)):
    return db.query(Rol).all()

from pydantic import BaseModel, EmailStr, validator, Field
from datetime import datetime
from typing import List
from .rol_schema import RolResponse

class UsuarioBase(BaseModel):
    nombre: str = Field(..., min_length=3, max_length=100, description="Nombre del usuario")
    email: EmailStr
    telefono: str | None = Field(None, max_length=20)

class UsuarioCreate(UsuarioBase):
    # use a Python-friendly field name; this maps to DB column `contraseña`
    contrasena: str = Field(..., min_length=6, description="Contraseña (mínimo 6 caracteres)")
    roles: List[int] | None = None
    
    @validator('nombre')
    def nombre_no_vacio(cls, v):
        if not v.strip():
            raise ValueError('El nombre no puede estar vacío')
        return v.strip()

class UsuarioResponse(UsuarioBase):
    id_usuario: int
    roles: List[RolResponse]
    solicitud_rol: str | None = None
    rol_solicitado: int | None = None
    estado: str
    fecha_registro: datetime
    class Config:
        orm_mode = True

class UsuarioUpdate(BaseModel):
    nombre: str | None = None
    email: EmailStr | None = None
    telefono: str | None = None
    estado: str | None = None

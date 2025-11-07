from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from core.database import Base

class UsuarioRol(Base):
    __tablename__ = "usuario_roles"
    usuario_id = Column(Integer, ForeignKey("usuarios.id_usuario"), primary_key=True)
    rol_id = Column(Integer, ForeignKey("roles.id_rol"), primary_key=True)

    usuario = relationship("Usuario", back_populates="roles")
    rol = relationship("Rol")

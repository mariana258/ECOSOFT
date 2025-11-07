from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from core.database import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id_usuario = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    telefono = Column(String(20))
    # map the DB column named with ñ to a Python-friendly attribute
    contrasena = Column("contraseña", String(255), nullable=False)
    estado = Column(String(20), default="activo")
    fecha_registro = Column(DateTime, default=datetime.utcnow)
    solicitud_rol = Column(Enum('ninguna','pendiente','aprobada','rechazada'), default='ninguna')
    rol_solicitado = Column(Integer, ForeignKey("roles.id_rol"), nullable=True)

    roles = relationship("UsuarioRol", back_populates="usuario")

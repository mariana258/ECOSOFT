from sqlalchemy import Column, Integer, DateTime, DECIMAL, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from core.database import Base

class HistorialInventario(Base):
    __tablename__ = 'historial_inventario'

    id_historial = Column(Integer, primary_key=True, index=True)
    id_material = Column(Integer, ForeignKey('materiales.id_material'), nullable=False)
    id_usuario_operacion = Column(Integer, ForeignKey('usuarios.id_usuario'), nullable=False)
    rol_usuario = Column(Enum('cliente','proveedor'), nullable=False)
    id_vendedor = Column(Integer, ForeignKey('usuarios.id_usuario'), nullable=False)
    fecha_hora = Column(DateTime, default=datetime.utcnow)
    cantidad_antes = Column(DECIMAL(10,2), nullable=False)
    cantidad_despues = Column(DECIMAL(10,2), nullable=False)
    precio_compra = Column(DECIMAL(10,2), nullable=False)
    precio_venta = Column(DECIMAL(10,2), nullable=False)

    material = relationship('Material')
    usuario_operacion = relationship('Usuario', foreign_keys=[id_usuario_operacion])
    vendedor = relationship('Usuario', foreign_keys=[id_vendedor])

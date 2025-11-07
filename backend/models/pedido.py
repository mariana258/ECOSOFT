from sqlalchemy import Column, Integer, DateTime, DECIMAL, Enum, ForeignKey, Text
from sqlalchemy.orm import relationship
from core.database import Base
from datetime import datetime
import enum
class EstadoPedido(enum.Enum):
    pendiente = 'pendiente'
    en_proceso = 'en proceso'
    completado = 'completado'
    cancelado = 'cancelado'
class Pedido(Base):
    __tablename__ = 'pedidos'
    id_pedido = Column(Integer, primary_key=True, index=True)
    id_cliente = Column(Integer, ForeignKey('usuarios.id_usuario'), nullable=False)
    id_vendedor = Column(Integer, ForeignKey('usuarios.id_usuario'), nullable=True)
    fecha_pedido = Column(DateTime, default=datetime.utcnow)
    fecha_programada = Column(DateTime, nullable=True)
    estado = Column(Enum(EstadoPedido), default=EstadoPedido.pendiente)
    total = Column(DECIMAL(10,2), default=0)
    observaciones = Column(Text)
    detalles = relationship('DetallePedido', back_populates='pedido', cascade='all, delete-orphan')
    factura = relationship('Factura', back_populates='pedido', uselist=False)

from sqlalchemy import Column, Integer, ForeignKey, DateTime, DECIMAL, Enum
from sqlalchemy.orm import relationship
from core.database import Base
from datetime import datetime
import enum
class EstadoFactura(enum.Enum):
    pagada = 'pagada'
    pendiente = 'pendiente'
    anulada = 'anulada'
class MetodoPago(enum.Enum):
    efectivo = 'efectivo'
    transferencia = 'transferencia'
    tarjeta = 'tarjeta'
class Factura(Base):
    __tablename__ = 'facturas'
    id_factura = Column(Integer, primary_key=True, index=True)
    id_pedido = Column(Integer, ForeignKey('pedidos.id_pedido'), nullable=False, unique=True)
    fecha_emision = Column(DateTime, default=datetime.utcnow)
    total = Column(DECIMAL(10,2), nullable=False)
    metodo_pago = Column(Enum(MetodoPago), nullable=False)
    estado = Column(Enum(EstadoFactura), default=EstadoFactura.pendiente)
    pedido = relationship('Pedido', back_populates='factura')
    pagos = relationship('Pago', back_populates='factura', cascade='all, delete-orphan')

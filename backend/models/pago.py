from sqlalchemy import Column, Integer, ForeignKey, DateTime, DECIMAL, String
from sqlalchemy.orm import relationship
from core.database import Base
from datetime import datetime
class Pago(Base):
    __tablename__ = 'pagos'
    id_pago = Column(Integer, primary_key=True, index=True)
    id_factura = Column(Integer, ForeignKey('facturas.id_factura'), nullable=False)
    fecha_pago = Column(DateTime, default=datetime.utcnow)
    monto = Column(DECIMAL(10,2), nullable=False)
    comprobante = Column(String(255), nullable=True)
    factura = relationship('Factura', back_populates='pagos')

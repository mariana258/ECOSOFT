from sqlalchemy import Column, Integer, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship
from core.database import Base
class DetallePedido(Base):
    __tablename__ = 'detalle_pedido'
    id_detalle = Column(Integer, primary_key=True, index=True)
    id_pedido = Column(Integer, ForeignKey('pedidos.id_pedido'), nullable=False)
    id_material = Column(Integer, ForeignKey('materiales.id_material'), nullable=False)
    cantidad = Column(DECIMAL(10,2), nullable=False)
    precio_unitario = Column(DECIMAL(10,2), nullable=False)
    pedido = relationship('Pedido', back_populates='detalles')

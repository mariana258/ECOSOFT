from sqlalchemy import Column, Integer, DECIMAL, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from core.database import Base

class Inventario(Base):
    __tablename__ = "inventario"

    id_inventario = Column(Integer, primary_key=True, index=True)
    id_material = Column(Integer, ForeignKey("materiales.id_material"), unique=True)
    cantidad = Column(DECIMAL(10,2), default=0)
    stock_minimo = Column(DECIMAL(10,2), default=0)
    ultima_actualizacion = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    material = relationship("Material", back_populates="inventario")

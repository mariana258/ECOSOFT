from sqlalchemy import Column, Integer, String, Text, Enum, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship
from core.database import Base

class Material(Base):
    __tablename__ = "materiales"

    id_material = Column(Integer, primary_key=True, index=True)
    id_proveedor = Column(Integer, ForeignKey("usuarios.id_usuario"), nullable=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text)
    unidad_medida = Column(String(20), nullable=False)
    precio_compra = Column(DECIMAL(10,2), nullable=False)
    precio_venta = Column(DECIMAL(10,2), nullable=False)
    tipo = Column(Enum("entrada","salida"), nullable=False)

    inventario = relationship("Inventario", uselist=False, back_populates="material")

from pydantic import BaseModel, Field
from decimal import Decimal

class InventarioBase(BaseModel):
    id_material: int
    cantidad: Decimal = Field(..., ge=0, description="La cantidad no puede ser negativa")
    stock_minimo: Decimal = Field(..., ge=0, description="El stock mínimo no puede ser negativo")

class InventarioResponse(InventarioBase):
    id_inventario: int
    class Config:
        orm_mode = True

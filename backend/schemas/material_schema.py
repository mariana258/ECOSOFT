from pydantic import BaseModel, validator, Field
from decimal import Decimal

class MaterialBase(BaseModel):
    id_proveedor: int | None = None
    nombre: str = Field(..., min_length=3, max_length=100)
    descripcion: str | None = Field(None, max_length=500)
    unidad_medida: str = Field(..., max_length=20)
    precio_compra: Decimal = Field(..., gt=0, description="Precio de compra debe ser mayor a 0")
    precio_venta: Decimal = Field(..., gt=0, description="Precio de venta debe ser mayor a 0")
    tipo: str = Field(..., max_length=50)
    
    @validator('precio_venta')
    def precio_venta_mayor_compra(cls, v, values):
        if 'precio_compra' in values and v < values['precio_compra']:
            raise ValueError('El precio de venta debe ser mayor o igual al precio de compra')
        return v

class MaterialResponse(MaterialBase):
    id_material: int
    class Config:
        orm_mode = True

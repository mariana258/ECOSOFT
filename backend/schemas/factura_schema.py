from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal
class FacturaBase(BaseModel):
    id_pedido: int
    total: Decimal
    metodo_pago: str
class FacturaResponse(FacturaBase):
    id_factura: int
    fecha_emision: datetime
    estado: str
    class Config:
        orm_mode = True

class FacturaUpdate(BaseModel):
    total: Decimal | None = None
    metodo_pago: str | None = None
    estado: str | None = None

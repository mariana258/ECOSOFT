from pydantic import BaseModel, Field
from datetime import datetime
from decimal import Decimal

class PagoBase(BaseModel):
    id_factura: int
    monto: Decimal = Field(..., gt=0, description="El monto debe ser mayor a 0")
    comprobante: str | None = Field(None, max_length=200)
class PagoResponse(PagoBase):
    id_pago: int
    fecha_pago: datetime
    class Config:
        orm_mode = True

class PagoUpdate(BaseModel):
    monto: Decimal | None = None
    comprobante: str | None = None

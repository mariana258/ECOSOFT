from pydantic import BaseModel
from typing import List
from datetime import datetime
from decimal import Decimal
class PedidoBase(BaseModel):
    id_cliente: int
    id_vendedor: int | None = None
    fecha_programada: datetime | None = None
    observaciones: str | None = None
class PedidoCreate(PedidoBase):
    detalles: List[dict]
class PedidoResponse(PedidoBase):
    id_pedido: int
    fecha_pedido: datetime
    estado: str
    total: Decimal
    class Config:
        orm_mode = True

class PedidoUpdate(BaseModel):
    id_vendedor: int | None = None
    fecha_programada: datetime | None = None
    observaciones: str | None = None
    estado: str | None = None

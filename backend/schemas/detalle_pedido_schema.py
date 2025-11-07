from pydantic import BaseModel
from decimal import Decimal
class DetallePedidoBase(BaseModel):
    id_pedido: int
    id_material: int
    cantidad: Decimal
    precio_unitario: Decimal
class DetallePedidoResponse(DetallePedidoBase):
    id_detalle: int
    class Config:
        orm_mode = True

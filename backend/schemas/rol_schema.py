from pydantic import BaseModel
class RolBase(BaseModel):
    nombre: str
    descripcion: str | None = None
class RolResponse(RolBase):
    id_rol: int
    class Config:
        orm_mode = True

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.database import get_db
from core.security import get_current_user, require_roles
from models import Pedido, DetallePedido, Material, Usuario
from schemas.pedido_schema import PedidoCreate, PedidoResponse, PedidoUpdate
from decimal import Decimal
router = APIRouter()

@router.post('/', response_model=PedidoResponse, status_code=status.HTTP_201_CREATED)
def crear_pedido(
    payload: PedidoCreate, 
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    pedido = Pedido(id_cliente=payload.id_cliente, id_vendedor=payload.id_vendedor, fecha_programada=payload.fecha_programada, observaciones=payload.observaciones)
    try:
        db.add(pedido)
        db.commit()
        db.refresh(pedido)
        
        for d in payload.detalles:
            mat = db.query(Material).filter(Material.id_material == d['id_material']).first()
            if not mat:
                db.delete(pedido)
                db.commit()
                raise HTTPException(status_code=400, detail=f"Material {d['id_material']} no encontrado")
            # use material's selling price as unit price
            detalle = DetallePedido(id_pedido=pedido.id_pedido, id_material=d['id_material'], cantidad=Decimal(str(d['cantidad'])), precio_unitario=mat.precio_venta)
            db.add(detalle)
        
        db.commit()
        db.refresh(pedido)
        
        total = db.query(DetallePedido).filter(DetallePedido.id_pedido == pedido.id_pedido).with_entities((DetallePedido.cantidad * DetallePedido.precio_unitario).label('st')).all()
        suma = sum([float(r.st) for r in total]) if total else 0
        pedido.total = suma
        db.commit()
        db.refresh(pedido)
        return pedido
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get('/', response_model=list[PedidoResponse])
def listar_pedidos(db: Session = Depends(get_db)):
    return db.query(Pedido).all()

@router.get('/{id_pedido}', response_model=PedidoResponse)
def obtener_pedido(id_pedido: int, db: Session = Depends(get_db)):
    """Obtener un pedido por ID"""
    pedido = db.query(Pedido).filter(Pedido.id_pedido == id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=404, detail='Pedido no encontrado')
    return pedido

@router.put('/{id_pedido}', response_model=PedidoResponse)
def actualizar_pedido(
    id_pedido: int, 
    payload: PedidoUpdate, 
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_roles(['administrador', 'vendedor']))
):
    """Actualizar un pedido"""
    pedido = db.query(Pedido).filter(Pedido.id_pedido == id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=404, detail='Pedido no encontrado')
    
    try:
        if payload.id_vendedor is not None:
            pedido.id_vendedor = payload.id_vendedor
        if payload.fecha_programada is not None:
            pedido.fecha_programada = payload.fecha_programada
        if payload.observaciones is not None:
            pedido.observaciones = payload.observaciones
        if payload.estado is not None:
            pedido.estado = payload.estado
        
        db.commit()
        db.refresh(pedido)
        return pedido
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.delete('/{id_pedido}', status_code=status.HTTP_204_NO_CONTENT)
def eliminar_pedido(
    id_pedido: int, 
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_roles(['administrador']))
):
    """Eliminar un pedido y sus detalles (cascade automático)"""
    pedido = db.query(Pedido).filter(Pedido.id_pedido == id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=404, detail='Pedido no encontrado')
    
    try:
        db.delete(pedido)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

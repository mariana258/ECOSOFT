from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.database import get_db
from core.security import get_current_user, require_roles
from models import Factura, Pedido, Pago, Usuario
from schemas.factura_schema import FacturaBase, FacturaResponse, FacturaUpdate
from decimal import Decimal
router = APIRouter()

@router.post('/', response_model=FacturaResponse, status_code=status.HTTP_201_CREATED)
def crear_factura(
    payload: FacturaBase, 
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_roles(['administrador', 'vendedor']))
):
    pedido = db.query(Pedido).filter(Pedido.id_pedido == payload.id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=404, detail='Pedido no encontrado')
    if db.query(Factura).filter(Factura.id_pedido == payload.id_pedido).first():
        raise HTTPException(status_code=400, detail='Factura ya creada para este pedido')
    try:
        factura = Factura(id_pedido=payload.id_pedido, total=Decimal(str(payload.total)), metodo_pago=payload.metodo_pago)
        db.add(factura)
        db.commit()
        db.refresh(factura)
        return factura
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get('/', response_model=list[FacturaResponse])
def listar_facturas(db: Session = Depends(get_db)):
    return db.query(Factura).all()

@router.get('/{id_factura}', response_model=FacturaResponse)
def obtener_factura(id_factura: int, db: Session = Depends(get_db)):
    """Obtener una factura por ID"""
    factura = db.query(Factura).filter(Factura.id_factura == id_factura).first()
    if not factura:
        raise HTTPException(status_code=404, detail='Factura no encontrada')
    return factura

@router.put('/{id_factura}', response_model=FacturaResponse)
def actualizar_factura(
    id_factura: int, 
    payload: FacturaUpdate, 
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_roles(['administrador', 'vendedor']))
):
    """Actualizar una factura"""
    factura = db.query(Factura).filter(Factura.id_factura == id_factura).first()
    if not factura:
        raise HTTPException(status_code=404, detail='Factura no encontrada')
    
    try:
        if payload.total is not None:
            factura.total = Decimal(str(payload.total))
        if payload.metodo_pago is not None:
            factura.metodo_pago = payload.metodo_pago
        if payload.estado is not None:
            factura.estado = payload.estado
        
        db.commit()
        db.refresh(factura)
        return factura
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.delete('/{id_factura}', status_code=status.HTTP_204_NO_CONTENT)
def eliminar_factura(
    id_factura: int, 
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_roles(['administrador']))
):
    """Eliminar una factura y sus pagos (cascade automático)"""
    factura = db.query(Factura).filter(Factura.id_factura == id_factura).first()
    if not factura:
        raise HTTPException(status_code=404, detail='Factura no encontrada')
    
    try:
        db.delete(factura)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

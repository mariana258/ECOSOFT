from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.database import get_db
from core.security import get_current_user, require_roles
from models import Pago, Factura, Usuario
from schemas.pago_schema import PagoBase, PagoResponse, PagoUpdate
from decimal import Decimal
router = APIRouter()

@router.post('/', response_model=PagoResponse, status_code=status.HTTP_201_CREATED)
def crear_pago(
    payload: PagoBase, 
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    factura = db.query(Factura).filter(Factura.id_factura == payload.id_factura).first()
    if not factura:
        raise HTTPException(status_code=404, detail='Factura no encontrada')
    try:
        pago = Pago(id_factura=payload.id_factura, monto=Decimal(str(payload.monto)), comprobante=payload.comprobante)
        db.add(pago)
        db.commit()
        db.refresh(pago)
        return pago
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get('/', response_model=list[PagoResponse])
def listar_pagos(db: Session = Depends(get_db)):
    return db.query(Pago).all()

@router.get('/{id_pago}', response_model=PagoResponse)
def obtener_pago(id_pago: int, db: Session = Depends(get_db)):
    """Obtener un pago por ID"""
    pago = db.query(Pago).filter(Pago.id_pago == id_pago).first()
    if not pago:
        raise HTTPException(status_code=404, detail='Pago no encontrado')
    return pago

@router.put('/{id_pago}', response_model=PagoResponse)
def actualizar_pago(
    id_pago: int, 
    payload: PagoUpdate, 
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_roles(['administrador', 'vendedor']))
):
    """Actualizar un pago"""
    pago = db.query(Pago).filter(Pago.id_pago == id_pago).first()
    if not pago:
        raise HTTPException(status_code=404, detail='Pago no encontrado')
    
    try:
        if payload.monto is not None:
            pago.monto = Decimal(str(payload.monto))
        if payload.comprobante is not None:
            pago.comprobante = payload.comprobante
        
        db.commit()
        db.refresh(pago)
        return pago
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.delete('/{id_pago}', status_code=status.HTTP_204_NO_CONTENT)
def eliminar_pago(
    id_pago: int, 
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_roles(['administrador']))
):
    """Eliminar un pago"""
    pago = db.query(Pago).filter(Pago.id_pago == id_pago).first()
    if not pago:
        raise HTTPException(status_code=404, detail='Pago no encontrado')
    
    try:
        db.delete(pago)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.database import get_db
from core.security import get_current_user, require_roles
from models import Material, Inventario, Usuario
from schemas.material_schema import MaterialBase, MaterialResponse
router = APIRouter()
@router.post('/', response_model=MaterialResponse)
def crear_material(
    payload: MaterialBase, 
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_roles(['administrador', 'vendedor']))
):
    try:
        mat = Material(id_proveedor=payload.id_proveedor, nombre=payload.nombre, descripcion=payload.descripcion, unidad_medida=payload.unidad_medida, precio_compra=payload.precio_compra, precio_venta=payload.precio_venta, tipo=payload.tipo)
        db.add(mat)
        db.commit(); db.refresh(mat)
        if not db.query(Inventario).filter(Inventario.id_material == mat.id_material).first():
            inv = Inventario(id_material=mat.id_material, cantidad=0, stock_minimo=0)
            db.add(inv); db.commit()
        return mat
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
@router.get('/', response_model=list[MaterialResponse])
def listar_materiales(db: Session = Depends(get_db)):
    return db.query(Material).all()


@router.get('/{id_material}', response_model=MaterialResponse)
def obtener_material(id_material: int, db: Session = Depends(get_db)):
    mat = db.query(Material).filter(Material.id_material == id_material).first()
    if not mat:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Material no encontrado')
    return mat


@router.put('/{id_material}', response_model=MaterialResponse)
def actualizar_material(
    id_material: int, 
    payload: MaterialBase, 
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_roles(['administrador', 'vendedor']))
):
    mat = db.query(Material).filter(Material.id_material == id_material).first()
    if not mat:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Material no encontrado')
    try:
        mat.nombre = payload.nombre
        mat.descripcion = payload.descripcion
        mat.unidad_medida = payload.unidad_medida
        mat.precio_compra = payload.precio_compra
        mat.precio_venta = payload.precio_venta
        mat.tipo = payload.tipo
        db.commit(); db.refresh(mat)
        return mat
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.delete('/{id_material}', status_code=status.HTTP_204_NO_CONTENT)
def eliminar_material(
    id_material: int, 
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_roles(['administrador']))
):
    mat = db.query(Material).filter(Material.id_material == id_material).first()
    if not mat:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Material no encontrado')
    try:
        # optionally delete inventory record
        db.query(Inventario).filter(Inventario.id_material == id_material).delete()
        db.delete(mat)
        db.commit()
        return
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

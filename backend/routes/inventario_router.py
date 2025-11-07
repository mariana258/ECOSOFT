from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import get_db
from core.security import get_current_user
from models import Inventario, Usuario, Rol, Material, HistorialInventario
from schemas.inventario_schema import InventarioBase, InventarioResponse
from decimal import Decimal
router = APIRouter()
@router.get('/', response_model=list[InventarioResponse])
def listar_inventario(db: Session = Depends(get_db)):
    return db.query(Inventario).all()


@router.get('/{id_material}', response_model=InventarioResponse)
def obtener_inventario(id_material: int, db: Session = Depends(get_db)):
    inv = db.query(Inventario).filter(Inventario.id_material == id_material).first()
    if not inv:
        raise HTTPException(status_code=404, detail='Inventario no encontrado')
    return inv


@router.get('/historial/{id_material}')
def listar_historial(id_material: int, db: Session = Depends(get_db)):
    registros = db.query(HistorialInventario).filter(HistorialInventario.id_material == id_material).order_by(HistorialInventario.fecha_hora.desc()).all()
    data = []
    for r in registros:
        data.append({
            'id_historial': r.id_historial,
            'id_material': r.id_material,
            'id_usuario_operacion': r.id_usuario_operacion,
            'rol_usuario': r.rol_usuario,
            'id_vendedor': r.id_vendedor,
            'fecha_hora': r.fecha_hora.isoformat() if r.fecha_hora else None,
            'cantidad_antes': float(r.cantidad_antes),
            'cantidad_despues': float(r.cantidad_despues),
            'precio_compra': float(r.precio_compra),
            'precio_venta': float(r.precio_venta)
        })
    return data
@router.post('/ajustar')
def ajustar_stock(
    id_material: int, 
    cantidad: Decimal, 
    accion: str, 
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    inv = db.query(Inventario).filter(Inventario.id_material == id_material).first()
    if not inv:
        raise HTTPException(status_code=404, detail='Inventario no encontrado')
    
    user_roles = [r.nombre.lower() for r in current_user.roles]
    # preserve previous quantity for historial
    cantidad_antes = inv.cantidad
    if 'administrador' in user_roles:
        pass
    elif accion == 'restar':
        if 'cliente' not in user_roles and 'vendedor' not in user_roles:
            raise HTTPException(status_code=403, detail='No autorizado a restar stock')
        if cantidad < 1:
            raise HTTPException(status_code=400, detail='Cliente debe restar al menos 1')
        if inv.cantidad - cantidad < 0:
            raise HTTPException(status_code=400, detail='Stock insuficiente')
        inv.cantidad = inv.cantidad - cantidad
    elif accion == 'sumar':
        if 'proveedor' not in user_roles and 'vendedor' not in user_roles:
            raise HTTPException(status_code=403, detail='No autorizado a sumar stock')
        inv.cantidad = inv.cantidad + cantidad
    else:
        raise HTTPException(status_code=400, detail='Accion inválida')
    db.commit()
    db.refresh(inv)

    # add a historial record reflecting the movement
    mat = db.query(Material).filter(Material.id_material == id_material).first()
    precio_compra = mat.precio_compra if mat and hasattr(mat, 'precio_compra') else 0
    precio_venta = mat.precio_venta if mat and hasattr(mat, 'precio_venta') else 0
    # determine rol_usuario for historial: restar->cliente, sumar->proveedor
    rol_usuario = 'cliente' if accion == 'restar' else 'proveedor'
    id_vendedor = current_user.id_usuario
    historial = HistorialInventario(
        id_material=id_material,
        id_usuario_operacion=current_user.id_usuario,
        rol_usuario=rol_usuario,
        id_vendedor=id_vendedor,
        cantidad_antes=cantidad_antes,
        cantidad_despues=inv.cantidad,
        precio_compra=precio_compra,
        precio_venta=precio_venta
    )
    db.add(historial)
    db.commit()

    return {'detail':'Stock ajustado', 'id_material': id_material, 'cantidad': float(inv.cantidad)}

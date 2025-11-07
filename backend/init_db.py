"""
Script para inicializar datos base en la base de datos
Crear roles por defecto
"""
from sqlalchemy.orm import Session
from core.database import SessionLocal, engine, Base
from models import Rol
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_roles(db: Session):
    """Crear roles por defecto si no existen"""
    roles_default = [
        {"nombre": "Administrador", "descripcion": "Acceso total al sistema"},
        {"nombre": "Vendedor", "descripcion": "Puede gestionar ventas, pedidos y materiales"},
        {"nombre": "Cliente", "descripcion": "Puede realizar pedidos y ver su información"},
        {"nombre": "Proveedor", "descripcion": "Puede agregar stock al inventario"},
    ]
    
    for rol_data in roles_default:
        existing = db.query(Rol).filter(Rol.nombre.ilike(rol_data["nombre"])).first()
        if not existing:
            rol = Rol(nombre=rol_data["nombre"], descripcion=rol_data["descripcion"])
            db.add(rol)
            logger.info(f"✅ Rol creado: {rol_data['nombre']}")
        else:
            logger.info(f"⏭️  Rol ya existe: {rol_data['nombre']}")
    
    db.commit()

def init_db():
    """Inicializar base de datos"""
    logger.info("Iniciando creación de tablas...")
    
    # Crear todas las tablas
    Base.metadata.create_all(bind=engine)
    logger.info("✅ Tablas creadas")
    
    # Crear roles por defecto
    db = SessionLocal()
    try:
        logger.info("Creando roles por defecto...")
        init_roles(db)
        logger.info("✅ Inicialización completada")
    except Exception as e:
        logger.error(f"❌ Error durante la inicialización: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_db()

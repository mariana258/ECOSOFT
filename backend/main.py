from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError
from core.database import Base, engine
from core.middleware import (
    log_requests_middleware,
    validation_exception_handler,
    sqlalchemy_exception_handler,
    general_exception_handler
)
import models


def _create_db_tables_safely():
    """Create DB tables but catch errors so the app can still start when DB is down.

    This prevents uvicorn from crashing during module import if the MySQL server
    is not available in local dev environments. The actual creation is executed
    on FastAPI startup.
    """
    import logging
    logger = logging.getLogger(__name__)
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created/verified successfully")
    except Exception as exc:
        # Don't raise: allow the app to start and handle DB errors at request time.
        logger.warning(f"Could not create/verify DB tables at startup: {exc}")


app = FastAPI(
    title='Ecosoft - Inventario Reciclaje (v3)', 
    version='3.0',
    description='API REST para sistema de gestión de inventario de reciclaje',
    contact={
        "name": "Ecosoft ",
        
    }
)

# Middlewares
app.add_middleware(
    CORSMiddleware, 
    allow_origins=['*'], 
    allow_credentials=True, 
    allow_methods=['*'], 
    allow_headers=['*']
)
app.middleware("http")(log_requests_middleware)

# Exception handlers
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(SQLAlchemyError, sqlalchemy_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

# Routers
from routes.auth_router import router as auth_router
from routes.rol_router import router as rol_router
from routes.usuario_router import router as usuario_router
from routes.material_router import router as material_router
from routes.inventario_router import router as inventario_router
from routes.pedido_router import router as pedido_router
from routes.factura_router import router as factura_router
from routes.pago_router import router as pago_router

app.include_router(auth_router, prefix="/auth", tags=["Autenticación"])
app.include_router(rol_router, prefix="/rol", tags=["Roles"])
app.include_router(usuario_router, prefix="/usuario", tags=["Usuarios"])
app.include_router(material_router, prefix="/material", tags=["Materiales"])
app.include_router(inventario_router, prefix="/inventario", tags=["Inventario"])
app.include_router(pedido_router, prefix="/pedido", tags=["Pedidos"])
app.include_router(factura_router, prefix="/factura", tags=["Facturas"])
app.include_router(pago_router, prefix="/pago", tags=["Pagos"])



@app.on_event("startup")
def on_startup():
    # Try to create tables at startup but keep the application alive if it fails.
    _create_db_tables_safely()


@app.get('/')
def root():
    return {'message': 'Ecosoft API v3 funcionando'}


@app.get('/health')
def health_check():
    """Endpoint de health check para verificar el estado del servidor"""
    return {
        'status': 'healthy',
        'service': 'Ecosoft API',
        'version': '3.0'
    }

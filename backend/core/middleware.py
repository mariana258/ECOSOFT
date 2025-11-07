"""
Middleware para manejo global de errores y logging
"""
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError
import logging
from datetime import datetime

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def log_requests_middleware(request: Request, call_next):
    """Middleware para registrar todas las peticiones"""
    start_time = datetime.utcnow()
    
    # Log request
    logger.info(f"Petición: {request.method} {request.url.path}")
    
    response = await call_next(request)
    
    # Log response
    process_time = (datetime.utcnow() - start_time).total_seconds()
    logger.info(
        f"Respuesta: {request.method} {request.url.path} "
        f"- Status: {response.status_code} - Tiempo: {process_time:.3f}s"
    )
    
    return response

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handler para errores de validación de Pydantic"""
    logger.error(f"Error de validación en {request.url.path}: {exc.errors()}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": "Error de validación",
            "errors": exc.errors()
        }
    )

async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    """Handler para errores de base de datos"""
    logger.error(f"Error de base de datos en {request.url.path}: {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "Error de base de datos",
            "message": "Ocurrió un error al procesar la solicitud"
        }
    )

async def general_exception_handler(request: Request, exc: Exception):
    """Handler para errores generales no capturados"""
    logger.error(f"Error no manejado en {request.url.path}: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "Error interno del servidor",
            "message": str(exc) if isinstance(exc, ValueError) else "Ocurrió un error inesperado"
        }
    )

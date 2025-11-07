import redis
import json
from typing import Any
from core.config import REDIS_HOST, REDIS_PORT
import logging

logger = logging.getLogger(__name__)

try:
    redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, decode_responses=True)
    # Test connection
    redis_client.ping()
    REDIS_AVAILABLE = True
    logger.info("Redis conectado exitosamente")
except Exception as e:
    REDIS_AVAILABLE = False
    redis_client = None
    logger.warning(f"Redis no disponible: {e}. El caché estará deshabilitado.")

def get_from_cache(key: str) -> Any:
    """Obtener valor del caché"""
    if not REDIS_AVAILABLE or not redis_client:
        return None
    try:
        value = redis_client.get(key)
        if value:
            return json.loads(value)
        return None
    except Exception as e:
        logger.error(f"Error al obtener del caché: {e}")
        return None

def save_to_cache(key: str, value: Any, ttl: int = 300):
    """Guardar valor en el caché con TTL en segundos"""
    if not REDIS_AVAILABLE or not redis_client:
        return False
    try:
        redis_client.setex(key, ttl, json.dumps(value))
        return True
    except Exception as e:
        logger.error(f"Error al guardar en caché: {e}")
        return False

def delete_from_cache(key: str):
    """Eliminar valor del caché"""
    if not REDIS_AVAILABLE or not redis_client:
        return False
    try:
        redis_client.delete(key)
        return True
    except Exception as e:
        logger.error(f"Error al eliminar del caché: {e}")
        return False

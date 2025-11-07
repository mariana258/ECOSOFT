from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from core.database import get_db
from core.security import (
    verify_password, 
    create_access_token, 
    create_refresh_token,
    verify_token,
    get_current_user
)
from core.config import ACCESS_TOKEN_EXPIRE_MINUTES
from models.usuario import Usuario
from schemas.auth_schema import TokenResponse, RefreshTokenRequest, UserInfo
from jose import JWTError

router = APIRouter()

@router.post('/login', response_model=TokenResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Login endpoint - usa email en el campo username"""
    user = db.query(Usuario).filter(Usuario.email == form_data.username).first()
    
    if not user or not verify_password(form_data.password, user.contrasena):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if user.estado != 'activo':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario inactivo"
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id_usuario)}, 
        expires_delta=access_token_expires
    )
    refresh_token = create_refresh_token(data={"sub": str(user.id_usuario)})
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@router.post('/refresh', response_model=TokenResponse)
def refresh_token(payload: RefreshTokenRequest, db: Session = Depends(get_db)):
    """Renovar access token usando refresh token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Refresh token inválido",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        token_data = verify_token(payload.refresh_token, credentials_exception)
        if token_data.get("type") != "refresh":
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user_id = int(token_data.get("sub"))
    user = db.query(Usuario).filter(Usuario.id_usuario == user_id).first()
    
    if not user or user.estado != 'activo':
        raise credentials_exception
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id_usuario)}, 
        expires_delta=access_token_expires
    )
    new_refresh_token = create_refresh_token(data={"sub": str(user.id_usuario)})
    
    return {
        "access_token": access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer"
    }

@router.get('/me', response_model=UserInfo)
def get_current_user_info(current_user: Usuario = Depends(get_current_user)):
    """Obtener información del usuario autenticado"""
    return {
        "id_usuario": current_user.id_usuario,
        "nombre": current_user.nombre,
        "email": current_user.email,
        "roles": [rol.nombre for rol in current_user.roles]
    }

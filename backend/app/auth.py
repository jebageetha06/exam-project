from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import jwt, JWTError
import os
from datetime import datetime, timedelta
from .database import get_db
from . import models

SECRET = os.getenv("JWT_SECRET", "Jebageetha123")
ALG = os.getenv("JWT_ALG", "HS256")
EXPIRE_MIN = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(p: str) -> str:
    return pwd_ctx.hash(p)

def verify_password(p: str, ph: str) -> bool:
    return pwd_ctx.verify(p, ph)

def create_access_token(sub: str):
    payload = {"sub": sub, "exp": datetime.utcnow() + timedelta(minutes=EXPIRE_MIN)}
    return jwt.encode(payload, SECRET, algorithm=ALG)

def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)) -> models.User:
    cred_exc = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    try:
        payload = jwt.decode(token, SECRET, algorithms=[ALG])
        email = payload.get("sub")
        if not email:
            raise cred_exc
    except JWTError:
        raise cred_exc
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise cred_exc
    return user

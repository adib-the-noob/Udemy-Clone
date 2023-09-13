from fastapi import HTTPException, status

from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt


from config import settings
from db import db_dependency
from models.user_model import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def authenticate_user(
    username: str | None, email: str | None, password: str, db: db_dependency
) -> bool:
    user = db.query(User).filter(User.username == username).first()
    if not user:
        user = db.query(User).filter(User.email == email).first()
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def create_user(email: str, password: str, full_name: str, db: db_dependency):
    if email is not None:
        user = db.query(User).filter(User.email == email).first()
        if user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )
        user = User(
            email=email,
            hashed_password=hash_password(password),
            full_name=full_name,
        )
        user.set_username()
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

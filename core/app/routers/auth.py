from typing import Annotated
import os
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse

from jose import jwt, JWTError
from config import settings


from utils.auth_utils import (
    authenticate_user,
    create_user,
    create_access_token,
    get_current_user,
)

from db import db_dependency

from schemas.auth_schemas import Token, UserRequest, UserResponse
from schemas import profile_schemas
from models.user_model import User, Profile

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

current_user = Annotated[User, Depends(get_current_user)]

@router.post("/create-user", response_model=Token, status_code=status.HTTP_201_CREATED)
async def register(user: UserRequest, db: db_dependency):
    user = create_user(
        email=user.email,
        password=user.password,
        phone_number=user.phone_number,
        full_name=user.full_name,
        db=db,
    )
    token = create_access_token(
        data={"sub": user.email, "id": user.id}
    )
    return {
        "access_token": token,
        "token_type": "bearer",
    }

@router.post("/token", response_model=None)
async def user_login(
    form_data : Annotated[OAuth2PasswordRequestForm, Depends()],
    db: db_dependency
):
    if form_data.username is None and form_data.email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    user = authenticate_user(
        email=form_data.username, 
        password=form_data.password, 
        db=db 
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    token = create_access_token(
        data={"sub": user.email, "id": user.id}
    )
    return {
        "access_token": token,
        "token_type": "bearer",
        "data" : {
            "id" : user.id,
            "username" : user.username,
            "email" : user.email,
        }
    }


@router.get("/me", response_model=UserResponse)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_user)],
    db: db_dependency
  ):
    return JSONResponse({
        "data" : {
            "id" : current_user.id,
            "username" : current_user.username,
            "email" : current_user.email,
            "phone_number" : current_user.phone_number,
        }
    })

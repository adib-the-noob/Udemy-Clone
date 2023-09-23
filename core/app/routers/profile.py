from typing import Annotated, Optional
import os
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from fastapi.responses import JSONResponse

from jose import jwt, JWTError
from config import settings


from utils.auth_utils import (
    get_current_user,
)

from db import db_dependency

from schemas import profile_schemas
from models.user_models import User
from models.profile_models import Profile

router = APIRouter(
    prefix="/profile",
    tags=["profile"],
)

current_user = Annotated[User, Depends(get_current_user)]


@router.post("/create-profile", response_model=profile_schemas.ProfileResponse)
def create_profile(
    user: current_user,
    db: db_dependency,
    # profile : profile_schemas.ProfileRequest,
    address: str = Form(...),
    role : str = Form(...),
    profile_picture: UploadFile = File(None),
):
    if db.query(Profile).filter(Profile.user_id == user.id).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Profile already exists",
        )

    file_path = None
    if profile_picture is not None:
        if not os.path.exists("media/profile_pictures"):
            os.makedirs("media/profile_pictures")
        # create a media folder in the root directory
        with open(f"media/profile_pictures/{profile_picture.filename}", "wb") as buffer:
            buffer.write(profile_picture.file.read())
            file_path = (
                f"{settings.BASE_URL}/media/profile_pictures/{profile_picture.filename}"
            )
    
    profile = Profile(
        user_id=user.id,
        address=address,
        role=role,
        profile_picture=profile_picture.filename if profile_picture else None,
    )
    profile.save(db)

    return JSONResponse(
        {
            "data": {
                "id": profile.id,
                "user_id": profile.user_id,
                "address": profile.address,
                "profile_picture": file_path,
            }
        }
    )


@router.get("/get-profile", response_model=profile_schemas.ProfileResponse)
def get_profile(user: current_user, db: db_dependency):
    profile = db.query(Profile).filter(Profile.user_id == user.id).first()
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found",
        )
    return JSONResponse(
        {
            "data": {
                "address": profile.address,
                "role": profile.role,
                "profile_picture": profile.profile_picture_url(),
            }
        },
        status_code=status.HTTP_200_OK,
    )

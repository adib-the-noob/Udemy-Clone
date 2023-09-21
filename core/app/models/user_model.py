import random
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from db import Base  
from config import settings

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    full_name = Column(String)
    email = Column(String, unique=True, index=True)
    phone_number = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)

    profile = relationship("Profile", back_populates="user")

    def set_username(self):
        self.username = self.full_name.lower().replace(" ", "_") + str(random.randint(100, 999))


class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)
    
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="profile")
    
    role = Column(String, default="student")
    address = Column(String)
    profile_picture = Column(String)

    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    def save(self, db):
        db.add(self)
        db.commit()
        db.refresh(self)
        return self
    
    # make a property to return the profile picture url

    def profile_picture_url(self) -> str | None:
        return f"{settings.BASE_URL}/media/profile_pictures/{self.profile_picture}" if self.profile_picture else None
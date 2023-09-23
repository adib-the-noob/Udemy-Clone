import random
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from db import Base  
from config import settings

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
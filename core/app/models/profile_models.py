from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from db import Base  
from config import settings
from utils.db_utils.BaseModel import BaseModelMixin

class Profile(Base, BaseModelMixin):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)
    
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="profile")
    
    role = Column(String, default="student")
    address = Column(String)
    profile_picture = Column(String)

    # make a property to return the profile picture url

    def profile_picture_url(self) -> str | None:
        return f"{settings.BASE_URL}/media/profile_pictures/{self.profile_picture}" if self.profile_picture else None
    

class Education(Base, BaseModelMixin):
    __tablename__ = "educations"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"))   
    user = relationship("User", back_populates="education")

    institution_name = Column(String)
    degree = Column(String)
    graduated = Column(Boolean, default=False)

    starting_date = Column(DateTime)
    ending_date = Column(DateTime)
    
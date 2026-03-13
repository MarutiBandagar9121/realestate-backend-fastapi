from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base

class City(Base):
    __tablename__ = "cities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    state = Column(String(100), nullable=False)
    short_name = Column(String(100), unique=True, nullable=False)

    location = relationship("Location", back_populates="city")
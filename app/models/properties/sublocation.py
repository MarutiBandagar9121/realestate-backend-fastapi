
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Sublocation(Base):
    __tablename__ = "sublocations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    location_id = Column(Integer, ForeignKey("locations.id"), nullable=False)
    
    location = relationship("Location", back_populates="sublocations")
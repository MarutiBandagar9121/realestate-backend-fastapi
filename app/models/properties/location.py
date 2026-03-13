from app.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKey, Integer, String

class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    city_id = Column(Integer, ForeignKey("cities.id"), nullable=False)
    location_type_business = Column(String(100), nullable=False)
    city_division_name = Column(String(100), nullable=False)
    
    city = relationship("City", back_populates="locations")
from app.database import Base
from sqlalchemy import Column, Float, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class Property(Base):
    __tablename__ = "properties"

    id = Column(Integer, primary_key=True, index=True)
    project_name = Column(String(100), nullable=False)
    project_grade = Column(String(100), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    google_map_url = Column(String(500), nullable=False)
    address_line1 = Column(String(100), nullable=False)
    address_line2 = Column(String(100),nullable=True)
    city_id = Column(Integer, ForeignKey("cities.id"), nullable=False)
    location_id = Column(Integer, ForeignKey("locations.id"), nullable=False)
    sublocation_id = Column(Integer, ForeignKey("sublocations.id"), nullable=False)
    total_property_area = Column(Float, nullable=False)
    total_property_area_unit = Column(String(20), nullable=False)
    property_sanction_type = Column(String(100), nullable=False)
    property_type = Column(String(100), nullable=False)
    tenant_profile = Column(String(500), nullable=True)
       
    city = relationship("City", back_populates="properties")
    location = relationship("Location", back_populates="properties")
    sublocation = relationship("Sublocation", back_populates="properties")

    
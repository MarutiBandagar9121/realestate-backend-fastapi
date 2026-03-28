from uuid import UUID

from pydantic import BaseModel
from typing import Optional

# Property types
class PropertyTypeModel(BaseModel):
    id: int
    name: str

    model_config = {"from_attributes": True}

# ── Nested reference schemas (used inside responses) ─────────────────────────

class CityRef(BaseModel):
    id: int
    name: str

    model_config = {"from_attributes": True}


class LocationRef(BaseModel):
    id: int
    name: str

    model_config = {"from_attributes": True}


class SublocationRef(BaseModel):
    id: int
    name: str

    model_config = {"from_attributes": True}


class PropertyTypeRef(BaseModel):
    id: int
    name: str

    model_config = {"from_attributes": True}


# ── Request schemas ───────────────────────────────────────────────────────────

class PropertyCreate(BaseModel):
    project_name: str
    project_grade: str
    city_id: int
    location_id: int
    sublocation_id: int
    latitude: float
    longitude: float
    google_map_url: str
    address_line1: str
    address_line2: Optional[str] = None
    total_property_area: float
    total_property_area_unit: str
    property_sanction_type: str
    tenant_profile: Optional[str] = None
    property_type_id: int


class PropertyUpdate(BaseModel):
    """
    property_type_id is intentionally excluded.
    It cannot be changed after creation as it defines the node tree structure.
    """
    project_name: Optional[str] = None
    project_grade: Optional[str] = None
    city_id: Optional[int] = None
    location_id: Optional[int] = None
    sublocation_id: Optional[int] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    google_map_url: Optional[str] = None
    address_line1: Optional[str] = None
    address_line2: Optional[str] = None
    total_property_area: Optional[float] = None
    total_property_area_unit: Optional[str] = None
    property_sanction_type: Optional[str] = None
    tenant_profile: Optional[str] = None


# ── Response schema ───────────────────────────────────────────────────────────

class PropertyResponse(BaseModel):
    id: UUID
    project_name: str
    project_grade: str
    city: CityRef
    location: LocationRef
    sublocation: SublocationRef
    property_type: PropertyTypeRef
    latitude: float
    longitude: float
    google_map_url: str
    address_line1: str
    address_line2: Optional[str]
    total_property_area: float
    total_property_area_unit: str
    property_sanction_type: str
    tenant_profile: Optional[str]

    model_config = {"from_attributes": True}


# ── Paginated list response ───────────────────────────────────────────────────

class PropertyListResponse(BaseModel):
    items: list[PropertyResponse]
    total: int
    skip: int
    limit: int



from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime


# ── Shared node info (embedded in every detail response) ─────────────────────

class NodeInfo(BaseModel):
    id: UUID
    node_name: str
    property_id: int
    node_type_id: int
    node_type_name: str       # resolved name e.g. "BUILDING", "WING" etc.
    parent_node_id: Optional[UUID]
    sequence_order: int
    status: str
    created_at: datetime
    updated_at: datetime


# ── Generic node update (rename / reorder / status change) ───────────────────

class NodeUpdate(BaseModel):
    node_name: Optional[str] = None
    sequence_order: Optional[int] = None
    status: Optional[str] = None


# ── Tree response (recursive) ─────────────────────────────────────────────────

class NodeTreeItem(BaseModel):
    id: UUID
    node_name: str
    node_type_id: int
    node_type_name: str
    sequence_order: int
    status: str
    children: list["NodeTreeItem"] = []


NodeTreeItem.model_rebuild()


class PropertyTreeResponse(BaseModel):
    property_id: int
    nodes: list[NodeTreeItem]


# ── Building ──────────────────────────────────────────────────────────────────

class BuildingCreate(BaseModel):
    # node fields
    node_name: str
    sequence_order: int = 1
    # detail fields
    building_name: str
    grade: str
    year_built: int
    total_area: float
    total_area_unit: str
    power_backup: bool
    green_rating: str
    parking_ratio: str


class BuildingUpdate(BaseModel):
    # node fields
    node_name: Optional[str] = None
    sequence_order: Optional[int] = None
    # detail fields
    building_name: Optional[str] = None
    grade: Optional[str] = None
    year_built: Optional[int] = None
    total_area: Optional[float] = None
    total_area_unit: Optional[str] = None
    power_backup: Optional[bool] = None
    green_rating: Optional[str] = None
    parking_ratio: Optional[str] = None


class BuildingDetailResponse(BaseModel):
    building_name: str
    grade: str
    year_built: int
    total_area: float
    total_area_unit: str
    power_backup: bool
    green_rating: str
    parking_ratio: str


class BuildingResponse(BaseModel):
    node: NodeInfo
    detail: BuildingDetailResponse


# ── Wing ──────────────────────────────────────────────────────────────────────

class WingCreate(BaseModel):
    node_name: str
    sequence_order: int = 1
    wing_name: str
    independent_entrance: Optional[bool] = None


class WingUpdate(BaseModel):
    node_name: Optional[str] = None
    sequence_order: Optional[int] = None
    wing_name: Optional[str] = None
    independent_entrance: Optional[bool] = None


class WingDetailResponse(BaseModel):
    wing_name: str
    independent_entrance: Optional[bool]


class WingResponse(BaseModel):
    node: NodeInfo
    detail: WingDetailResponse


# ── Floor ─────────────────────────────────────────────────────────────────────

class FloorCreate(BaseModel):
    node_name: str
    sequence_order: int = 1
    floor_name: str
    floor_area: float
    floor_area_unit: str


class FloorUpdate(BaseModel):
    node_name: Optional[str] = None
    sequence_order: Optional[int] = None
    floor_name: Optional[str] = None
    floor_area: Optional[float] = None
    floor_area_unit: Optional[str] = None


class FloorDetailResponse(BaseModel):
    floor_name: str
    floor_area: float
    floor_area_unit: str


class FloorResponse(BaseModel):
    node: NodeInfo
    detail: FloorDetailResponse


# ── Unit ──────────────────────────────────────────────────────────────────────

class UnitCreate(BaseModel):
    node_name: str
    sequence_order: int = 1
    unit_name: str
    unit_area: float
    unit_area_unit: str
    chargeable_area: float
    chargeable_area_unit: str
    carpet_area: float
    carpet_area_unit: str
    rental: float
    rental_unit: str
    notice_period: int
    notice_period_unit: str
    cam_charges: float
    cam_charges_unit: str


class UnitUpdate(BaseModel):
    node_name: Optional[str] = None
    sequence_order: Optional[int] = None
    unit_name: Optional[str] = None
    unit_area: Optional[float] = None
    unit_area_unit: Optional[str] = None
    chargeable_area: Optional[float] = None
    chargeable_area_unit: Optional[str] = None
    carpet_area: Optional[float] = None
    carpet_area_unit: Optional[str] = None
    rental: Optional[float] = None
    rental_unit: Optional[str] = None
    notice_period: Optional[int] = None
    notice_period_unit: Optional[str] = None
    cam_charges: Optional[float] = None
    cam_charges_unit: Optional[str] = None


class UnitDetailResponse(BaseModel):
    unit_name: str
    unit_area: float
    unit_area_unit: str
    chargeable_area: float
    chargeable_area_unit: str
    carpet_area: float
    carpet_area_unit: str
    rental: float
    rental_unit: str
    notice_period: int
    notice_period_unit: str
    cam_charges: float
    cam_charges_unit: str


class UnitResponse(BaseModel):
    node: NodeInfo
    detail: UnitDetailResponse

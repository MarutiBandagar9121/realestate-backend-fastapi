from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.node import (
    NodeUpdate,
    BuildingCreate, BuildingUpdate, BuildingResponse,
    WingCreate, WingUpdate, WingResponse,
    FloorCreate, FloorUpdate, FloorResponse,
    UnitCreate, UnitUpdate, UnitResponse,
    PropertyTreeResponse,
)
from app.services import node_service

router = APIRouter(tags=["Property Nodes"])


# ── Tree ──────────────────────────────────────────────────────────────────────

@router.get(
    "/properties/{property_id}/nodes/tree",
    response_model=PropertyTreeResponse,
)
def get_property_tree(property_id: int, db: Session = Depends(get_db)):
    tree = node_service.get_property_tree(db, property_id)
    if tree is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Property not found")
    return tree


# ── Generic node (get / update / delete) ─────────────────────────────────────

@router.get("/nodes/{node_id}")
def get_node(node_id: UUID, db: Session = Depends(get_db)):
    node = node_service.get_node(db, node_id)
    if not node:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Node not found")
    return node


@router.patch("/nodes/{node_id}")
def update_node(node_id: UUID, data: NodeUpdate, db: Session = Depends(get_db)):
    node = node_service.update_node(db, node_id, data)
    if not node:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Node not found")
    return node


@router.delete("/nodes/{node_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_node(node_id: UUID, db: Session = Depends(get_db)):
    if not node_service.delete_node(db, node_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Node not found")


# ── Building ──────────────────────────────────────────────────────────────────

@router.post(
    "/properties/{property_id}/buildings",
    response_model=BuildingResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_building(property_id: int, data: BuildingCreate, db: Session = Depends(get_db)):
    try:
        return node_service.create_building(db, property_id, data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/nodes/{node_id}/building", response_model=BuildingResponse)
def get_building(node_id: UUID, db: Session = Depends(get_db)):
    result = node_service.get_building(db, node_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Building not found")
    return result


@router.patch("/nodes/{node_id}/building", response_model=BuildingResponse)
def update_building(node_id: UUID, data: BuildingUpdate, db: Session = Depends(get_db)):
    try:
        result = node_service.update_building(db, node_id, data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Building not found")
    return result


# ── Wing ──────────────────────────────────────────────────────────────────────

@router.post(
    "/nodes/{parent_node_id}/wings",
    response_model=WingResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_wing(parent_node_id: UUID, data: WingCreate, db: Session = Depends(get_db)):
    try:
        return node_service.create_wing(db, parent_node_id, data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/nodes/{node_id}/wing", response_model=WingResponse)
def get_wing(node_id: UUID, db: Session = Depends(get_db)):
    result = node_service.get_wing(db, node_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Wing not found")
    return result


@router.patch("/nodes/{node_id}/wing", response_model=WingResponse)
def update_wing(node_id: UUID, data: WingUpdate, db: Session = Depends(get_db)):
    try:
        result = node_service.update_wing(db, node_id, data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Wing not found")
    return result


# ── Floor ─────────────────────────────────────────────────────────────────────

@router.post(
    "/nodes/{parent_node_id}/floors",
    response_model=FloorResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_floor(parent_node_id: UUID, data: FloorCreate, db: Session = Depends(get_db)):
    try:
        return node_service.create_floor(db, parent_node_id, data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/nodes/{node_id}/floor", response_model=FloorResponse)
def get_floor(node_id: UUID, db: Session = Depends(get_db)):
    result = node_service.get_floor(db, node_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Floor not found")
    return result


@router.patch("/nodes/{node_id}/floor", response_model=FloorResponse)
def update_floor(node_id: UUID, data: FloorUpdate, db: Session = Depends(get_db)):
    try:
        result = node_service.update_floor(db, node_id, data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Floor not found")
    return result


# ── Unit ──────────────────────────────────────────────────────────────────────

@router.post(
    "/nodes/{parent_node_id}/units",
    response_model=UnitResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_unit(parent_node_id: UUID, data: UnitCreate, db: Session = Depends(get_db)):
    try:
        return node_service.create_unit(db, parent_node_id, data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/nodes/{node_id}/unit", response_model=UnitResponse)
def get_unit(node_id: UUID, db: Session = Depends(get_db)):
    result = node_service.get_unit(db, node_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Unit not found")
    return result


@router.patch("/nodes/{node_id}/unit", response_model=UnitResponse)
def update_unit(node_id: UUID, data: UnitUpdate, db: Session = Depends(get_db)):
    try:
        result = node_service.update_unit(db, node_id, data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Unit not found")
    return result

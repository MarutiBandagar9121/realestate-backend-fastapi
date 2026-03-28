from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.property import PropertyCreate, PropertyListResponse, PropertyTypeModel, PropertyUpdate, PropertyResponse
from app.services import property_service

router = APIRouter(prefix="/properties", tags=["Properties"])

# upload property
@router.post("/", response_model=PropertyResponse, status_code=status.HTTP_201_CREATED)
def create_property(data: PropertyCreate, db: Session = Depends(get_db)):
    try:
        return property_service.create_property(db, data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

# upload properties bulk
@router.post("/bulk", response_model=list[PropertyResponse], status_code=status.HTTP_201_CREATED)
def create_properties_bulk(data: list[PropertyCreate], db: Session = Depends(get_db)):
    try:
        return property_service.create_properties_bulk(db, data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

# Get all Property types
@router.get("/types", response_model=list[PropertyTypeModel])
def getPropertyTypes(db: Session = Depends(get_db)):
    try:
        return property_service.get_property_types(db)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
    
# Get all properties (paginated, with optional filters)
@router.get("/", response_model=PropertyListResponse)
def list_properties(
    skip: int = 0,
    limit: int = 20,
    city_ids: list[int] = Query(default=[]),
    location_ids: list[int] = Query(default=[]),
    property_type_ids: list[int] = Query(default=[]),
    db: Session = Depends(get_db),
):
    return property_service.get_properties(
        db,
        skip=skip,
        limit=limit,
        city_ids=city_ids or None,
        location_ids=location_ids or None,
        property_type_ids=property_type_ids or None,
    )


@router.get("/{property_id}", response_model=PropertyResponse)
def get_property(property_id: UUID, db: Session = Depends(get_db)):
    prop = property_service.get_property(db, property_id)
    if not prop:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Property not found")
    return prop


@router.patch("/{property_id}", response_model=PropertyResponse)
def update_property(property_id: UUID, data: PropertyUpdate, db: Session = Depends(get_db)):
    try:
        prop = property_service.update_property(db, property_id, data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    if not prop:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Property not found")
    return prop


@router.delete("/{property_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_property(property_id: UUID, db: Session = Depends(get_db)):
    if not property_service.delete_property(db, property_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Property not found")
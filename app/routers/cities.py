from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.city import CityResponse
from app.database import get_db
from app.services import city_service

router = APIRouter(tags=["Cities"])

@router.get("/cities", response_model=list[CityResponse])
async def get_cities(db: Session = Depends(get_db)):
    try:
        cities = city_service.get_cities(db)
        return cities
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
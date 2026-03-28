from pydantic import BaseModel

class LocationResponse(BaseModel):
    id: int
    name: str
    city_id: int
    location_type_business: str
    city_division_name: str
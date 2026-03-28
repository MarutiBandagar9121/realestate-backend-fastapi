from sqlalchemy.orm import Session
from app.models.properties.location import Location

def get_locations(db: Session):
    return db.query(Location).all()
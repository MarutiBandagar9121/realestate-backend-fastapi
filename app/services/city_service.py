from sqlalchemy.orm import Session
from app.models.properties.city import City

def get_cities(db: Session):
    return db.query(City).all()
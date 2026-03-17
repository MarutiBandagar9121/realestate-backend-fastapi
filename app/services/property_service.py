from sqlalchemy.orm import Session, selectinload
from sqlalchemy import select

from app.models.properties import Property, City, Location, Sublocation, PropertyType
from app.schemas.property import PropertyCreate, PropertyUpdate


def _load_property(db: Session, property_id: int) -> Property | None:
    """Fetch a property with all relationships eagerly loaded."""
    stmt = (
        select(Property)
        .options(
            selectinload(Property.city),
            selectinload(Property.location),
            selectinload(Property.sublocation),
            selectinload(Property.property_type),
        )
        .where(Property.id == property_id)
    )
    return db.execute(stmt).scalar_one_or_none()


def _validate_location_hierarchy(
    db: Session,
    city_id: int,
    location_id: int,
    sublocation_id: int,
) -> None:
    """Validate that city → location → sublocation form a valid hierarchy."""
    if not db.get(City, city_id):
        raise ValueError(f"City with id {city_id} not found")

    location = db.get(Location, location_id)
    if not location:
        raise ValueError(f"Location with id {location_id} not found")
    if location.city_id != city_id:
        raise ValueError("Location does not belong to the given city")

    sublocation = db.get(Sublocation, sublocation_id)
    if not sublocation:
        raise ValueError(f"Sublocation with id {sublocation_id} not found")
    if sublocation.location_id != location_id:
        raise ValueError("Sublocation does not belong to the given location")


def get_property(db: Session, property_id: int) -> Property | None:
    return _load_property(db, property_id)


def get_properties(db: Session, skip: int = 0, limit: int = 20) -> list[Property]:
    stmt = (
        select(Property)
        .options(
            selectinload(Property.city),
            selectinload(Property.location),
            selectinload(Property.sublocation),
            selectinload(Property.property_type),
        )
        .offset(skip)
        .limit(limit)
    )
    return list(db.execute(stmt).scalars().all())


def create_property(db: Session, data: PropertyCreate) -> Property:
    if not db.get(PropertyType, data.property_type_id):
        raise ValueError(f"Property type with id {data.property_type_id} not found")

    _validate_location_hierarchy(db, data.city_id, data.location_id, data.sublocation_id)

    prop = Property(**data.model_dump())
    db.add(prop)
    db.commit()
    db.refresh(prop)
    return _load_property(db, prop.id)


def update_property(db: Session, property_id: int, data: PropertyUpdate) -> Property | None:
    prop = db.get(Property, property_id)
    if not prop:
        return None

    update_data = data.model_dump(exclude_unset=True)

    # Validate location hierarchy only for the fields being changed
    city_id = update_data.get("city_id", prop.city_id)
    location_id = update_data.get("location_id", prop.location_id)
    sublocation_id = update_data.get("sublocation_id", prop.sublocation_id)

    if any(k in update_data for k in ("city_id", "location_id", "sublocation_id")):
        _validate_location_hierarchy(db, city_id, location_id, sublocation_id)

    for key, value in update_data.items():
        setattr(prop, key, value)

    db.commit()
    return _load_property(db, property_id)


def delete_property(db: Session, property_id: int) -> bool:
    prop = db.get(Property, property_id)
    if not prop:
        return False
    db.delete(prop)
    db.commit()
    return True

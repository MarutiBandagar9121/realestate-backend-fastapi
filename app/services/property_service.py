from uuid import UUID

from sqlalchemy.orm import Session, selectinload
from sqlalchemy import select, func

from app.models.properties import Property, City, Location, Sublocation, PropertyType
from app.schemas.property import PropertyCreate, PropertyUpdate


def _load_property(db: Session, property_id: UUID) -> Property | None:
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


def get_property(db: Session, property_id: UUID) -> Property | None:
    return _load_property(db, property_id)


def get_properties(
    db: Session,
    skip: int = 0,
    limit: int = 20,
    city_ids: list[int] | None = None,
    location_ids: list[int] | None = None,
    property_type_ids: list[int] | None = None,
) -> dict:
    # Start with base statements — one for data, one for count
    data_stmt = select(Property).options(
        selectinload(Property.city),
        selectinload(Property.location),
        selectinload(Property.sublocation),
        selectinload(Property.property_type),
    )
    count_stmt = select(func.count()).select_from(Property)
    print("Request to get all properties received")
    if city_ids is not None:
        print("city_ids"+str(city_ids))
    if location_ids is not None:
        print("location_ids"+str(location_ids))
    if(property_type_ids is not None):
        print("property_type_ids"+str(property_type_ids))

    # Apply the same filters to both statements
    if city_ids:
        data_stmt = data_stmt.where(Property.city_id.in_(city_ids))
        count_stmt = count_stmt.where(Property.city_id.in_(city_ids))
    if location_ids:
        data_stmt = data_stmt.where(Property.location_id.in_(location_ids))
        count_stmt = count_stmt.where(Property.location_id.in_(location_ids))
    if property_type_ids:
        data_stmt = data_stmt.where(Property.property_type_id.in_(property_type_ids))
        count_stmt = count_stmt.where(Property.property_type_id.in_(property_type_ids))

    total = db.execute(count_stmt).scalar_one()
    items = list(db.execute(data_stmt.offset(skip).limit(limit)).scalars().all())

    return {"items": items, "total": total, "skip": skip, "limit": limit}


def create_property(db: Session, data: PropertyCreate) -> Property:
    if not db.get(PropertyType, data.property_type_id):
        raise ValueError(f"Property type with id {data.property_type_id} not found")

    _validate_location_hierarchy(db, data.city_id, data.location_id, data.sublocation_id)

    prop = Property(**data.model_dump())
    db.add(prop)
    db.commit()
    db.refresh(prop)
    return _load_property(db, prop.id)

def create_properties_bulk(db: Session, data: list[PropertyCreate]) -> list[Property]:
    property_type_ids = {d.property_type_id for d in data}
    city_ids = {d.city_id for d in data}
    location_ids = {d.location_id for d in data}
    sublocation_ids = {d.sublocation_id for d in data}

    # Batch-validate property types
    found_pt_ids = set(db.execute(select(PropertyType.id).where(PropertyType.id.in_(property_type_ids))).scalars())
    missing = property_type_ids - found_pt_ids
    if missing:
        raise ValueError(f"Property type(s) not found: {missing}")

    # Batch-validate cities
    found_city_ids = set(db.execute(select(City.id).where(City.id.in_(city_ids))).scalars())
    missing = city_ids - found_city_ids
    if missing:
        raise ValueError(f"City/cities not found: {missing}")

    # Batch-validate locations and capture city mapping
    locations = db.execute(select(Location.id, Location.city_id).where(Location.id.in_(location_ids))).all()
    found_location_ids = {row.id for row in locations}
    missing = location_ids - found_location_ids
    if missing:
        raise ValueError(f"Location(s) not found: {missing}")
    location_city_map = {row.id: row.city_id for row in locations}

    # Batch-validate sublocations and capture location mapping
    sublocations = db.execute(select(Sublocation.id, Sublocation.location_id).where(Sublocation.id.in_(sublocation_ids))).all()
    found_sublocation_ids = {row.id for row in sublocations}
    missing = sublocation_ids - found_sublocation_ids
    if missing:
        raise ValueError(f"Sublocation(s) not found: {missing}")
    sublocation_location_map = {row.id: row.location_id for row in sublocations}

    # Cross-validate hierarchy in memory (no extra DB calls)
    for prop_data in data:
        if location_city_map[prop_data.location_id] != prop_data.city_id:
            raise ValueError(f"Location {prop_data.location_id} does not belong to city {prop_data.city_id}")
        if sublocation_location_map[prop_data.sublocation_id] != prop_data.location_id:
            raise ValueError(f"Sublocation {prop_data.sublocation_id} does not belong to location {prop_data.location_id}")

    # Bulk insert — flush to get DB-generated UUIDs, then commit
    properties = [Property(**d.model_dump()) for d in data]
    db.add_all(properties)
    db.flush()
    ids = [prop.id for prop in properties]
    db.commit()

    # Single query to load all inserted properties with relationships
    stmt = (
        select(Property)
        .options(
            selectinload(Property.city),
            selectinload(Property.location),
            selectinload(Property.sublocation),
            selectinload(Property.property_type),
        )
        .where(Property.id.in_(ids))
    )
    return list(db.execute(stmt).scalars().all())


def update_property(db: Session, property_id: UUID, data: PropertyUpdate) -> Property | None:
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


def delete_property(db: Session, property_id: UUID) -> bool:
    prop = db.get(Property, property_id)
    if not prop:
        return False
    db.delete(prop)
    db.commit()
    return True

def get_property_types(db: Session):
    return db.query(PropertyType).all()

import uuid
from datetime import datetime

from sqlalchemy.orm import Session, selectinload
from sqlalchemy import select

from app.models.properties import (
    Property, PropertyNode, NodeType,
    Building, Wing, Floor, Unit,
)
from app.schemas.node import (
    NodeUpdate,
    BuildingCreate, BuildingUpdate,
    WingCreate, WingUpdate,
    FloorCreate, FloorUpdate,
    UnitCreate, UnitUpdate,
)


# ── Allowed parent node types per node type ───────────────────────────────────

_ALLOWED_PARENTS: dict[str, list[str] | None] = {
    "BUILDING": None,
    "WING":     ["BUILDING"],
    "FLOOR":    ["BUILDING", "WING"],
    "UNIT":     ["FLOOR"],
}


# ── Internal helpers ──────────────────────────────────────────────────────────

def _get_node_type(db: Session, name: str) -> NodeType:
    node_type = db.execute(
        select(NodeType).where(NodeType.name == name)
    ).scalar_one_or_none()
    if not node_type:
        raise ValueError(f"Node type '{name}' not found in database")
    return node_type


def _load_node(db: Session, node_id: uuid.UUID) -> PropertyNode | None:
    return db.execute(
        select(PropertyNode)
        .options(selectinload(PropertyNode.node_type))
        .where(PropertyNode.id == node_id)
    ).scalar_one_or_none()


def _validate_parent(
    db: Session,
    parent_node_id: uuid.UUID | None,
    node_type_name: str,
    property_id: int,
) -> None:
    allowed = _ALLOWED_PARENTS[node_type_name]

    if allowed is None:
        if parent_node_id is not None:
            raise ValueError(f"{node_type_name} must be a root node — parent_node_id must be null")
        return

    if parent_node_id is None:
        raise ValueError(f"{node_type_name} requires a parent node")

    parent = _load_node(db, parent_node_id)
    if not parent:
        raise ValueError(f"Parent node {parent_node_id} not found")
    if parent.property_id != property_id:
        raise ValueError("Parent node belongs to a different property")
    if parent.node_type.name not in allowed:
        raise ValueError(
            f"{node_type_name} can only be placed under {allowed}, "
            f"but parent is {parent.node_type.name}"
        )


def _node_to_info(node: PropertyNode) -> dict:
    return {
        "id": node.id,
        "node_name": node.node_name,
        "property_id": node.property_id,
        "node_type_id": node.node_type_id,
        "node_type_name": node.node_type.name,
        "parent_node_id": node.parent_node_id,
        "sequence_order": node.sequence_order,
        "status": node.status,
        "created_at": node.created_at,
        "updated_at": node.updated_at,
    }


def _make_node(
    db: Session,
    property_id: int,
    node_type_name: str,
    node_name: str,
    sequence_order: int,
    parent_node_id: uuid.UUID | None,
) -> PropertyNode:
    node_type = _get_node_type(db, node_type_name)
    _validate_parent(db, parent_node_id, node_type_name, property_id)

    now = datetime.utcnow()
    node = PropertyNode(
        id=uuid.uuid4(),
        node_name=node_name,
        property_id=property_id,
        node_type_id=node_type.id,
        parent_node_id=parent_node_id,
        sequence_order=sequence_order,
        status="ACTIVE",
        created_at=now,
        updated_at=now,
    )
    db.add(node)
    db.flush()  # get node.id without committing yet
    return node


# ── Tree ──────────────────────────────────────────────────────────────────────

def get_property_tree(db: Session, property_id: int) -> dict | None:
    if not db.get(Property, property_id):
        return None

    nodes = db.execute(
        select(PropertyNode)
        .options(selectinload(PropertyNode.node_type))
        .where(PropertyNode.property_id == property_id)
    ).scalars().all()

    # Build lookup dict
    tree_map: dict = {
        node.id: {
            "id": node.id,
            "node_name": node.node_name,
            "node_type_id": node.node_type_id,
            "node_type_name": node.node_type.name,
            "sequence_order": node.sequence_order,
            "status": node.status,
            "children": [],
        }
        for node in nodes
    }

    roots = []
    for node in nodes:
        if node.parent_node_id is None:
            roots.append(tree_map[node.id])
        else:
            parent = tree_map.get(node.parent_node_id)
            if parent:
                parent["children"].append(tree_map[node.id])

    def sort_tree(items: list) -> None:
        items.sort(key=lambda x: x["sequence_order"])
        for item in items:
            sort_tree(item["children"])

    sort_tree(roots)
    return {"property_id": property_id, "nodes": roots}


# ── Generic node ──────────────────────────────────────────────────────────────

def get_node(db: Session, node_id: uuid.UUID) -> PropertyNode | None:
    return _load_node(db, node_id)


def update_node(db: Session, node_id: uuid.UUID, data: NodeUpdate) -> PropertyNode | None:
    node = db.get(PropertyNode, node_id)
    if not node:
        return None
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(node, key, value)
    node.updated_at = datetime.utcnow()
    db.commit()
    return _load_node(db, node_id)


def delete_node(db: Session, node_id: uuid.UUID) -> bool:
    node = db.get(PropertyNode, node_id)
    if not node:
        return False
    db.delete(node)
    db.commit()
    return True


# ── Building ──────────────────────────────────────────────────────────────────

def create_building(db: Session, property_id: int, data: BuildingCreate) -> dict:
    if not db.get(Property, property_id):
        raise ValueError(f"Property {property_id} not found")

    node = _make_node(db, property_id, "BUILDING", data.node_name, data.sequence_order, None)

    now = datetime.utcnow()
    building = Building(
        node_id=node.id,
        building_name=data.building_name,
        grade=data.grade,
        year_built=data.year_built,
        total_area=data.total_area,
        total_area_unit=data.total_area_unit,
        power_backup=data.power_backup,
        green_rating=data.green_rating,
        parking_ratio=data.parking_ratio,
        created_at=now,
        updated_at=now,
    )
    db.add(building)
    db.commit()
    db.refresh(node)
    db.refresh(building)
    return _building_response(db, node.id)


def get_building(db: Session, node_id: uuid.UUID) -> dict | None:
    return _building_response(db, node_id)


def update_building(db: Session, node_id: uuid.UUID, data: BuildingUpdate) -> dict | None:
    node = db.get(PropertyNode, node_id)
    if not node:
        return None

    update = data.model_dump(exclude_unset=True)

    node_fields = {"node_name", "sequence_order"}
    for key in node_fields & update.keys():
        setattr(node, key, update[key])
    node.updated_at = datetime.utcnow()

    building = db.execute(
        select(Building).where(Building.node_id == node_id)
    ).scalar_one_or_none()

    if building:
        detail_fields = {k: v for k, v in update.items() if k not in node_fields}
        for key, value in detail_fields.items():
            setattr(building, key, value)
        building.updated_at = datetime.utcnow()

    db.commit()
    return _building_response(db, node_id)


def _building_response(db: Session, node_id: uuid.UUID) -> dict | None:
    node = _load_node(db, node_id)
    building = db.execute(
        select(Building).where(Building.node_id == node_id)
    ).scalar_one_or_none()

    if not node or not building:
        return None

    return {
        "node": _node_to_info(node),
        "detail": {
            "building_name": building.building_name,
            "grade": building.grade,
            "year_built": building.year_built,
            "total_area": building.total_area,
            "total_area_unit": building.total_area_unit,
            "power_backup": building.power_backup,
            "green_rating": building.green_rating,
            "parking_ratio": building.parking_ratio,
        },
    }


# ── Wing ──────────────────────────────────────────────────────────────────────

def create_wing(db: Session, parent_node_id: uuid.UUID, data: WingCreate) -> dict:
    parent = _load_node(db, parent_node_id)
    if not parent:
        raise ValueError(f"Parent node {parent_node_id} not found")

    node = _make_node(db, parent.property_id, "WING", data.node_name, data.sequence_order, parent_node_id)

    now = datetime.utcnow()
    wing = Wing(
        node_id=node.id,
        wing_name=data.wing_name,
        independent_entrance=data.independent_entrance,
        created_at=now,
        updated_at=now,
    )
    db.add(wing)
    db.commit()
    db.refresh(node)
    return _wing_response(db, node.id)


def get_wing(db: Session, node_id: uuid.UUID) -> dict | None:
    return _wing_response(db, node_id)


def update_wing(db: Session, node_id: uuid.UUID, data: WingUpdate) -> dict | None:
    node = db.get(PropertyNode, node_id)
    if not node:
        return None

    update = data.model_dump(exclude_unset=True)
    node_fields = {"node_name", "sequence_order"}

    for key in node_fields & update.keys():
        setattr(node, key, update[key])
    node.updated_at = datetime.utcnow()

    wing = db.execute(select(Wing).where(Wing.node_id == node_id)).scalar_one_or_none()
    if wing:
        for key, value in {k: v for k, v in update.items() if k not in node_fields}.items():
            setattr(wing, key, value)
        wing.updated_at = datetime.utcnow()

    db.commit()
    return _wing_response(db, node_id)


def _wing_response(db: Session, node_id: uuid.UUID) -> dict | None:
    node = _load_node(db, node_id)
    wing = db.execute(select(Wing).where(Wing.node_id == node_id)).scalar_one_or_none()

    if not node or not wing:
        return None

    return {
        "node": _node_to_info(node),
        "detail": {
            "wing_name": wing.wing_name,
            "independent_entrance": wing.independent_entrance,
        },
    }


# ── Floor ─────────────────────────────────────────────────────────────────────

def create_floor(db: Session, parent_node_id: uuid.UUID, data: FloorCreate) -> dict:
    parent = _load_node(db, parent_node_id)
    if not parent:
        raise ValueError(f"Parent node {parent_node_id} not found")

    node = _make_node(db, parent.property_id, "FLOOR", data.node_name, data.sequence_order, parent_node_id)

    now = datetime.utcnow()
    floor = Floor(
        id=uuid.uuid4(),
        node_id=node.id,
        floor_name=data.floor_name,
        floor_area=data.floor_area,
        floor_area_unit=data.floor_area_unit,
        created_at=now,
        updated_at=now,
    )
    db.add(floor)
    db.commit()
    db.refresh(node)
    return _floor_response(db, node.id)


def get_floor(db: Session, node_id: uuid.UUID) -> dict | None:
    return _floor_response(db, node_id)


def update_floor(db: Session, node_id: uuid.UUID, data: FloorUpdate) -> dict | None:
    node = db.get(PropertyNode, node_id)
    if not node:
        return None

    update = data.model_dump(exclude_unset=True)
    node_fields = {"node_name", "sequence_order"}

    for key in node_fields & update.keys():
        setattr(node, key, update[key])
    node.updated_at = datetime.utcnow()

    floor = db.execute(select(Floor).where(Floor.node_id == node_id)).scalar_one_or_none()
    if floor:
        for key, value in {k: v for k, v in update.items() if k not in node_fields}.items():
            setattr(floor, key, value)
        floor.updated_at = datetime.utcnow()

    db.commit()
    return _floor_response(db, node_id)


def _floor_response(db: Session, node_id: uuid.UUID) -> dict | None:
    node = _load_node(db, node_id)
    floor = db.execute(select(Floor).where(Floor.node_id == node_id)).scalar_one_or_none()

    if not node or not floor:
        return None

    return {
        "node": _node_to_info(node),
        "detail": {
            "floor_name": floor.floor_name,
            "floor_area": floor.floor_area,
            "floor_area_unit": floor.floor_area_unit,
        },
    }


# ── Unit ──────────────────────────────────────────────────────────────────────

def create_unit(db: Session, parent_node_id: uuid.UUID, data: UnitCreate) -> dict:
    parent = _load_node(db, parent_node_id)
    if not parent:
        raise ValueError(f"Parent node {parent_node_id} not found")

    node = _make_node(db, parent.property_id, "UNIT", data.node_name, data.sequence_order, parent_node_id)

    now = datetime.utcnow()
    unit = Unit(
        id=uuid.uuid4(),
        node_id=node.id,
        unit_name=data.unit_name,
        unit_area=data.unit_area,
        unit_area_unit=data.unit_area_unit,
        chargeable_area=data.chargeable_area,
        chargeable_area_unit=data.chargeable_area_unit,
        carpet_area=data.carpet_area,
        carpet_area_unit=data.carpet_area_unit,
        rental=data.rental,
        rental_unit=data.rental_unit,
        notice_period=data.notice_period,
        notice_period_unit=data.notice_period_unit,
        cam_charges=data.cam_charges,
        cam_charges_unit=data.cam_charges_unit,
        created_at=now,
        updated_at=now,
    )
    db.add(unit)
    db.commit()
    db.refresh(node)
    return _unit_response(db, node.id)


def get_unit(db: Session, node_id: uuid.UUID) -> dict | None:
    return _unit_response(db, node_id)


def update_unit(db: Session, node_id: uuid.UUID, data: UnitUpdate) -> dict | None:
    node = db.get(PropertyNode, node_id)
    if not node:
        return None

    update = data.model_dump(exclude_unset=True)
    node_fields = {"node_name", "sequence_order"}

    for key in node_fields & update.keys():
        setattr(node, key, update[key])
    node.updated_at = datetime.utcnow()

    unit = db.execute(select(Unit).where(Unit.node_id == node_id)).scalar_one_or_none()
    if unit:
        for key, value in {k: v for k, v in update.items() if k not in node_fields}.items():
            setattr(unit, key, value)
        unit.updated_at = datetime.utcnow()

    db.commit()
    return _unit_response(db, node_id)


def _unit_response(db: Session, node_id: uuid.UUID) -> dict | None:
    node = _load_node(db, node_id)
    unit = db.execute(select(Unit).where(Unit.node_id == node_id)).scalar_one_or_none()

    if not node or not unit:
        return None

    return {
        "node": _node_to_info(node),
        "detail": {
            "unit_name": unit.unit_name,
            "unit_area": unit.unit_area,
            "unit_area_unit": unit.unit_area_unit,
            "chargeable_area": unit.chargeable_area,
            "chargeable_area_unit": unit.chargeable_area_unit,
            "carpet_area": unit.carpet_area,
            "carpet_area_unit": unit.carpet_area_unit,
            "rental": unit.rental,
            "rental_unit": unit.rental_unit,
            "notice_period": unit.notice_period,
            "notice_period_unit": unit.notice_period_unit,
            "cam_charges": unit.cam_charges,
            "cam_charges_unit": unit.cam_charges_unit,
        },
    }

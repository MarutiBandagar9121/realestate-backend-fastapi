# EstateHub – FastAPI Backend

## What This Project Is
Commercial real estate platform backend API for a real estate advisory/brokerage firm. Serves two frontends: a customer app (Next.js) and an employee app (Reactjs).

## Tech Stack
- **Framework:** FastAPI (Python 3.13)
- **ORM:** SQLAlchemy 2.0 (async-ready, use modern style)
- **Schema validation:** Pydantic v2
- **DB Migrations:** Alembic
- **Database:** PostgreSQL
- **Server:** Uvicorn
- **Config:** pydantic-settings reading from `.env`

## Project Structure
```
app/
  config.py          # Settings via pydantic-settings
  database.py        # SQLAlchemy engine, SessionLocal, get_db()
  models/
    properties/      # All property-related SQLAlchemy models
    users/           # User model
  routers/           # API route modules (one per domain)
  schemas/           # Pydantic request/response schemas
  services/          # Business logic layer
alembic/             # DB migrations
main.py              # FastAPI app entry point
```

## Core Data Model — Property Node Tree
The central design pattern is a **hierarchical property node tree**:

- `Property` → top-level real estate asset
- `PropertyNode` → tree node (Building > Wing > Floor > Unit, or Land/Industrial/Logistics as leaves)
- Each node has a corresponding **detail table** (one-to-one): `Building`, `Wing`, `Floor`, `Unit`, `Land`, `Industrial`, `Logistics`, `RetailUnit`
- `NodeType` controls what kind of node it is (lookup table)
- `PropertyType` controls the asset category (lookup table)

This allows one Property to have multiple buildings, floors, units in a tree. **Do not flatten this into per-type tables.**

## Business Verticals
- Office Space (traditional + coworking/shared)
- Retail Space
- Industrial Space
- Logistics/Warehousing
- Land Deals
- Investment assets (future: fractional ownership, REIT-like)

## Key Domain Rules
- One property can have multiple simultaneous offerings (lease, sale, investment) — never duplicate the physical asset
- Offerings attach to `PropertyNode` (and optionally `Property`)
- Users have roles: ADMIN, OFFICE_HEAD, TRANSACTION_MANAGER, BUSINESS_DEVELOPMENT_MANAGER, DATA_MANAGER, DATA_SURVEYOR, CUSTOMER
- CRM: integrates with Zoho CRM (webhook ingestion + API sync)

## Coding Conventions
- Use `get_db()` dependency injection for database sessions in all routes
- One router file per domain in `app/routers/`
- Schemas in `app/schemas/` — separate request and response schemas per domain
- Business logic in `app/services/` — keep route handlers thin
- Always use SQLAlchemy 2.0 style (`select()` statements, not `session.query()`)
- Integer PKs for lookup tables (City, Location, NodeType etc.), UUID for transactional entities (Property, PropertyNode, etc.)

## What NOT To Do
- Do not use old SQLAlchemy 1.x Query API (`session.query(...)`) — use `select()` statements
- Do not put business logic in route handlers
- Do not break the node tree model by flattening it
- Do not commit secrets or `.env` files

## Running Locally
```bash
uvicorn main:app --reload
```

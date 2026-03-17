"""adding seed data

Revision ID: c0c994b20ba0
Revises: f7b8854d42db
Create Date: 2026-03-17 12:56:38.003075

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c0c994b20ba0'
down_revision: Union[str, Sequence[str], None] = 'f7b8854d42db'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ── Cities ────────────────────────────────────────────────────────────────
    op.execute("""
        INSERT INTO cities (id, name, state, short_name) VALUES
        (1, 'Pune', 'Maharashtra', 'Pune')
        ON CONFLICT DO NOTHING
    """)

    # ── Locations ─────────────────────────────────────────────────────────────
    op.execute("""
        INSERT INTO locations (id, name, city_id, city_division_name, location_type_business) VALUES
        (1,  'Hinjewadi',     1, 'West Pune', 'Peripheral'),
        (2,  'Wakad',         1, 'West Pune', 'Secondary'),
        (3,  'Bavdhan',       1, 'West Pune', 'Peripheral'),
        (4,  'Chinchwad',     1, 'West Pune', 'Peripheral'),
        (5,  'Balewadi',      1, 'West Pune', 'Secondary'),
        (6,  'Pashan',        1, 'West Pune', 'Secondary'),
        (7,  'Baner',         1, 'West Pune', 'Secondary'),
        (8,  'Kothrud',       1, 'West Pune', 'Secondary'),
        (9,  'Pimpri',        1, 'West Pune', 'Peripheral'),
        (10, 'Aundh',         1, 'West Pune', 'Secondary'),
        (11, 'Erandwane',     1, 'West Pune', 'Secondary'),
        (12, 'Khadki',        1, 'West Pune', 'Secondary'),
        (13, 'Shivaji Nagar', 1, 'West Pune', 'Secondary'),
        (14, 'Peth Area',     1, 'West Pune', 'Secondary'),
        (15, 'Bund Garden',   1, 'West Pune', 'Secondary'),
        (16, 'Yerawada',      1, 'West Pune', 'Secondary'),
        (17, 'Koregaon Park', 1, 'West Pune', 'Secondary'),
        (18, 'Kalyani Nagar', 1, 'West Pune', 'Secondary'),
        (19, 'Viman Nagar',   1, 'West Pune', 'Secondary'),
        (20, 'Wanowrie',      1, 'West Pune', 'Secondary'),
        (21, 'Kharadi',       1, 'West Pune', 'Secondary'),
        (22, 'Hadapsar',      1, 'West Pune', 'Secondary'),
        (23, 'Wagholi',       1, 'West Pune', 'Secondary'),
        (24, 'Swargate',      1, 'West Pune', 'Secondary'),
        (25, 'Kondhwa',       1, 'West Pune', 'Secondary')
        ON CONFLICT DO NOTHING
    """)

    # ── Sublocations ──────────────────────────────────────────────────────────
    op.execute("""
        INSERT INTO sublocations (id, name, location_id) VALUES
        -- Hinjewadi (1)
        (1,  'Phase 1',              1),
        (2,  'Phase 2',              1),
        (3,  'Phase 3',              1),
        -- Wakad (2)
        (4,  'Aundh Hinjewadi Road', 2),
        (5,  'Pimple Saudagar',      2),
        (6,  'Pimple Nilakh',        2),
        (7,  'Pimple Garav',         2),
        (8,  'Tathawade',            2),
        (9,  'Ravet',                2),
        -- Bavdhan (3)
        (10, 'Bhugaon',              3),
        (11, 'NDA Pashan Road',      3),
        -- Chinchwad (4)
        (12, 'Akurdi',               4),
        (13, 'Nigdi',                4),
        (14, 'Talwade',              4),
        -- Balewadi (5)
        (15, 'Cummins India Road',   5),
        (16, 'Mahalunge',            5),
        -- Pashan (6)
        (17, 'Pashan Sus Road',      6),
        -- Baner (7)
        (18, 'Baner Road',           7),
        (19, 'Mum-Bang Highway',     7),
        -- Kothrud (8)
        (20, 'Karve Nagar',          8),
        (21, 'Paud Road',            8),
        (22, 'Chandni Chowk',        8),
        (23, 'Sinhagad Road',        8),
        (24, 'Nanded',               8),
        (25, 'Warje',                8),
        -- Pimpri (9)
        (26, 'Kasarwadi',            9),
        (27, 'Bhosari',              9),
        (28, 'Moshi',                9),
        -- Aundh (10)
        (29, 'ITI Road',             10),
        (30, 'University Road',      10),
        (31, 'Bapodi',               10),
        -- Erandwane (11)
        (32, 'Prabhat Road',         11),
        (33, 'Law College Road',     11),
        -- Khadki (12)
        (34, 'Khadki',               12),
        -- Shivaji Nagar (13)
        (35, 'Wakdewadi',            13),
        (36, 'S B Road',             13),
        (37, 'Model Colony',         13),
        (38, 'FC Road',              13),
        (39, 'JM Road',              13),
        (40, 'Bhandarkar Road',      13),
        (41, 'Ganeshkhind Road',     13),
        -- Peth Area (14)
        (42, 'Sadashiv Peth',        14),
        (43, 'Raviwar Peth',         14),
        (44, 'Mangalwar Peth',       14),
        (45, 'Agarkar Nagar',        14),
        (46, 'Budhwar Peth',         14),
        (47, 'Pune Contonment',      14),
        -- Bund Garden (15)
        (48, 'Sangamvadi',           15),
        (49, 'Camp',                 15),
        -- Yerawada (16)
        (50, 'Vishrant Wadi',        16),
        (51, 'Tingre Nagar',         16),
        (52, 'Golf Club Road',       16),
        -- Koregaon Park (17)
        (53, 'North Main Road',      17),
        (54, 'Mundhwa',              17),
        -- Kalyani Nagar (18)
        (55, 'Kalyani Nagar',        18),
        -- Viman Nagar (19)
        (56, 'Wadgaon Sheri',        19),
        (57, 'Ramwadi',              19),
        -- Wanowrie (20)
        (58, 'Wanowrie',             20),
        -- Kharadi (21)
        (59, 'Eon Free Zone',        21),
        (60, 'Grant Road',           21),
        (61, 'Kharadi Mundhwa Road', 21),
        -- Hadapsar (22)
        (62, 'Magarpatta',           22),
        (63, 'Amanora',              22),
        (64, 'Fursungi',             22),
        (65, 'Solapur Road',         22),
        -- Wagholi (23)
        (66, 'Wagholi',              23),
        -- Swargate (24)
        (67, 'Gultekdi',             24),
        (68, 'Bibwewadi',            24),
        (69, 'Katraj',               24),
        (70, 'Shankar Sheth Road',   24),
        -- Kondhwa (25)
        (71, 'Nimb',                 25),
        (72, 'Undri',                25),
        (73, 'Lulla Nagar',          25)
        ON CONFLICT DO NOTHING
    """)

    # ── Property Types ────────────────────────────────────────────────────────
    op.execute("""
        INSERT INTO property_types (id, name) VALUES
        (1, 'Office_Commercial_Space'),
        (2, 'Standalone_Retail'),
        (3, 'Mall'),
        (4, 'Land'),
        (5, 'Logistics'),
        (6, 'Industrial')
        ON CONFLICT DO NOTHING
    """)

    # ── Node Types ────────────────────────────────────────────────────────────
    op.execute("""
        INSERT INTO node_types (id, name) VALUES
        (1, 'BUILDING'),
        (2, 'WING'),
        (3, 'FLOOR'),
        (4, 'UNIT'),
        (5, 'LAND'),
        (6, 'INDUSTRIAL'),
        (7, 'LOGISTICS'),
        (8, 'RETAIL_UNIT'),
        (9, 'SHARED_OFFICE')
        ON CONFLICT DO NOTHING
    """)


def downgrade() -> None:
    # Delete in reverse FK order to respect constraints
    op.execute("DELETE FROM sublocations WHERE id BETWEEN 1 AND 73")
    op.execute("DELETE FROM locations WHERE id BETWEEN 1 AND 25")
    op.execute("DELETE FROM cities WHERE id = 1")
    op.execute("DELETE FROM property_types WHERE id BETWEEN 1 AND 6")
    op.execute("DELETE FROM node_types WHERE id BETWEEN 1 AND 9")

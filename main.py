from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import properties, nodes, cities, locations

app = FastAPI(title="EstateHub API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(properties.router, prefix="/api/v1")
app.include_router(nodes.router, prefix="/api/v1")
app.include_router(cities.router, prefix="/api/v1")
app.include_router(locations.router, prefix="/api/v1")



@app.get("/")
def home():
    return {"message": "EstateHub API is running"}
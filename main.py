from fastapi import FastAPI
from app.routers import properties, nodes

app = FastAPI(title="EstateHub API", version="1.0.0")

app.include_router(properties.router, prefix="/api/v1")
app.include_router(nodes.router, prefix="/api/v1")


@app.get("/")
def home():
    return {"message": "EstateHub API is running"}
import fastapi
from app.config import Settings

app=fastapi.FastAPI()

@app.get("/")
def home():
    return {"message":"Estatehub Test API is working fine!"}
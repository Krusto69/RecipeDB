from fastapi import FastAPI
from routers import recipes

app = FastAPI()

@app.get("/")
def home():
    return {"message": "RecipeDB API is running"}

app.include_router(recipes.router)
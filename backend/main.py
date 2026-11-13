from fastapi import FastAPI
from backend.routers import recipes, ingredients

app = FastAPI()

@app.get("/")
def home():
    return {"message": "RecipeDB API is running"}

app.include_router(recipes.router)
app.include_router(ingredients.router)
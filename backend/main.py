from fastapi import FastAPI

from backend.routers import ingredients, recipes, steps, tags

app = FastAPI()

@app.get("/")
def home():
    return {"message": "RecipeDB API is running"}

app.include_router(recipes.router)
app.include_router(ingredients.router)
app.include_router(steps.router)
app.include_router(tags.router)
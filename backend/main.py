from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "RecipeDB API is running"}
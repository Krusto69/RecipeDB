from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database import SessionLocal
from backend.dependencies import get_db
from backend.models import Recipe
from backend.schemas import RecipeCreate, RecipeResponse, RecipeUpdate

router = APIRouter()




# CREATE
@router.post("/recipes", response_model=RecipeResponse, status_code=201)
def create_recipe(recipe: RecipeCreate, db: Session = Depends(get_db)):
    db_recipe = Recipe(**recipe.model_dump())#?

    db.add(db_recipe)
    db.commit()
    db.refresh(db_recipe)#?

    return db_recipe


# READ ALL
@router.get("/recipes", response_model=list[RecipeResponse])
def get_recipes(db: Session = Depends(get_db)):
    return db.query(Recipe).all()


# READ ONE
@router.get("/recipes/{recipe_id}", response_model=RecipeResponse)
def get_recipe(recipe_id: int, db: Session = Depends(get_db)):
    recipe = db.get(Recipe, recipe_id)

    if recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")

    return recipe


# UPDATE
@router.put("/recipes/{recipe_id}", response_model=RecipeResponse)
def update_recipe(
    recipe_id: int,
    recipe_data: RecipeUpdate,
    db: Session = Depends(get_db),
):
    recipe = db.get(Recipe, recipe_id)

    if recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")

    update_data = recipe_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(recipe, field, value)

    db.commit()
    db.refresh(recipe)

    return recipe


# DELETE
@router.delete("/recipes/{recipe_id}", status_code=204)
def delete_recipe(recipe_id: int, db: Session = Depends(get_db)):
    recipe = db.get(Recipe, recipe_id)

    if recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")

    db.delete(recipe)
    db.commit()

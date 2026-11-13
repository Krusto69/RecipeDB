from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database import SessionLocal
from backend.dependencies import get_db
from backend.models import Recipe, RecipeIngredient
from backend.schemas import IngredientCreate, IngredientResponse, IngredientUpdate

router = APIRouter()


@router.post(
    "/recipes/{recipe_id}/ingredients",
    response_model=IngredientResponse,
    status_code=201
)
def create_ingredient(
    recipe_id: int,
    ingredient: IngredientCreate,
    db: Session = Depends(get_db)
):
    recipe = db.get(Recipe, recipe_id)

    if recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")

    db_ingredient = RecipeIngredient(
        recipe_id=recipe_id,
        **ingredient.model_dump()
    )

    db.add(db_ingredient)
    db.commit()
    db.refresh(db_ingredient)

    return db_ingredient


@router.get(
    "/recipes/{recipe_id}/ingredients",
    response_model=list[IngredientResponse]
)
def get_ingredients(recipe_id: int, db: Session = Depends(get_db)):
    recipe = db.get(Recipe, recipe_id)

    if recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")

    return (
        db.query(RecipeIngredient)
        .filter(RecipeIngredient.recipe_id == recipe_id)
        .all()
    )


@router.put(
    "/recipes/{recipe_id}/ingredients/{ingredient_id}",
    response_model=IngredientResponse
)
def update_ingredient(
    recipe_id: int,
    ingredient_id: int,
    ingredient_data: IngredientUpdate,
    db: Session = Depends(get_db)
):
    recipe = db.get(Recipe, recipe_id)

    if recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")

    ingredient = db.get(RecipeIngredient, ingredient_id)

    if ingredient is None or ingredient.recipe_id != recipe_id:
        raise HTTPException(status_code=404, detail="Ingredient not found")

    update_data = ingredient_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(ingredient, field, value)

    db.commit()
    db.refresh(ingredient)

    return ingredient


@router.delete(
    "/recipes/{recipe_id}/ingredients/{ingredient_id}",
    status_code=204
)
def delete_ingredient(
    recipe_id: int,
    ingredient_id: int,
    db: Session = Depends(get_db)
):
    recipe = db.get(Recipe, recipe_id)

    if recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")

    ingredient = db.get(RecipeIngredient, ingredient_id)

    if ingredient is None or ingredient.recipe_id != recipe_id:
        raise HTTPException(status_code=404, detail="Ingredient not found")

    db.delete(ingredient)
    db.commit()
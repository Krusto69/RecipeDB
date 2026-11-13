from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.dependencies import get_db
from backend.models import Rating, Recipe
from backend.schemas import RatingCreate, RatingResponse, RatingUpdate

router = APIRouter()


@router.post(
    "/recipes/{recipe_id}/rating",
    response_model=RatingResponse,
    status_code=201
)
def create_rating(
    recipe_id: int,
    rating: RatingCreate,
    db: Session = Depends(get_db)
):
    recipe = db.get(Recipe, recipe_id)

    if recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")

    if recipe.rating is not None:
        raise HTTPException(status_code=409, detail="Recipe already has a rating")

    db_rating = Rating(
        recipe_id=recipe_id,
        **rating.model_dump()
    )

    db.add(db_rating)
    db.commit()
    db.refresh(db_rating)

    return db_rating


@router.get("/recipes/{recipe_id}/rating", response_model=RatingResponse)
def get_rating(recipe_id: int, db: Session = Depends(get_db)):
    recipe = db.get(Recipe, recipe_id)

    if recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")

    if recipe.rating is None:
        raise HTTPException(status_code=404, detail="Rating not found")

    return recipe.rating


@router.put("/recipes/{recipe_id}/rating", response_model=RatingResponse)
def update_rating(
    recipe_id: int,
    rating_data: RatingUpdate,
    db: Session = Depends(get_db)
):
    recipe = db.get(Recipe, recipe_id)

    if recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")

    if recipe.rating is None:
        raise HTTPException(status_code=404, detail="Rating not found")

    update_data = rating_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(recipe.rating, field, value)

    db.commit()
    db.refresh(recipe.rating)

    return recipe.rating


@router.delete("/recipes/{recipe_id}/rating", status_code=204)
def delete_rating(recipe_id: int, db: Session = Depends(get_db)):
    recipe = db.get(Recipe, recipe_id)

    if recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")

    if recipe.rating is None:
        raise HTTPException(status_code=404, detail="Rating not found")

    db.delete(recipe.rating)
    db.commit()
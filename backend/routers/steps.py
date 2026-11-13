from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from backend.dependencies import get_db
from backend.models import Recipe, RecipeStep
from backend.schemas import StepCreate, StepResponse, StepUpdate

router = APIRouter()

@router.post(
    "/recipes/{recipe_id}/steps",
    response_model=StepResponse,
    status_code=201
)
def create_step(
    recipe_id: int,
    step: StepCreate,
    db: Session = Depends(get_db)
):
    recipe = db.get(Recipe, recipe_id)
    if recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")

    db_step = RecipeStep(
        recipe_id=recipe_id,
        **step.model_dump()
    )

    db.add(db_step)

    try:
        db.commit()
        db.refresh(db_step)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Step number already exists for this recipe"
        )


    return db_step

@router.get(
    "/recipes/{recipe_id}/steps",
    response_model=list[StepResponse]
)
def get_steps(recipe_id: int, db: Session = Depends(get_db)):
    recipe = db.get(Recipe, recipe_id)
    if recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")

    return (
        db.query(RecipeStep)
        .filter(RecipeStep.recipe_id == recipe_id)
        .order_by(RecipeStep.step_number)
        .all()
    )


@router.put(
    "/recipes/{recipe_id}/steps/{step_id}",
    response_model=StepResponse
)
def update_step(
    recipe_id: int,
    step_id: int,
    step_data: StepUpdate,
    db: Session = Depends(get_db)
):
    recipe = db.get(Recipe, recipe_id)
    if recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")

    step = db.get(RecipeStep, step_id)
    if step is None or step.recipe_id != recipe_id:
        raise HTTPException(status_code=404, detail="Step not found")

    update_data = step_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(step, field, value)

    db.commit()
    db.refresh(step)

    return step


@router.delete(
    "/recipes/{recipe_id}/steps/{step_id}",
    status_code=204
)
def delete_step(
    recipe_id: int,
    step_id: int,
    db: Session = Depends(get_db)
):
    recipe = db.get(Recipe, recipe_id)
    if recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")

    step = db.get(RecipeStep, step_id)
    if step is None or step.recipe_id != recipe_id:
        raise HTTPException(status_code=404, detail="Step not found")

    db.delete(step)
    db.commit()
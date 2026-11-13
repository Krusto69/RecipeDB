from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from backend.dependencies import get_db
from backend.models import Recipe, Tag
from backend.schemas import TagCreate, TagResponse, TagUpdate

router = APIRouter()

@router.post("/tags", response_model=TagResponse, status_code=201)
def create_tag(tag: TagCreate, db: Session = Depends(get_db)):
    db_tag = Tag(**tag.model_dump())

    db.add(db_tag)

    try:
        db.commit()
        db.refresh(db_tag)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Tag already exists"
        )

    return db_tag



@router.get("/tags", response_model=list[TagResponse])
def get_tags(db: Session = Depends(get_db)):
    return db.query(Tag).all()


@router.get("/tags/{tag_id}", response_model=TagResponse)
def get_tag(tag_id: int, db: Session = Depends(get_db)):
    tag = db.get(Tag, tag_id)

    if tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")

    return tag



@router.put("/tags/{tag_id}", response_model=TagResponse)
def update_tag(
    tag_id: int,
    tag_data: TagUpdate,
    db: Session = Depends(get_db)
):
    tag = db.get(Tag, tag_id)

    if tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")

    update_data = tag_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(tag, field, value)

    try:
        db.commit()
        db.refresh(tag)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Tag name already exists"
        )

    return tag



@router.delete("/tags/{tag_id}", status_code=204)
def delete_tag(tag_id: int, db: Session = Depends(get_db)):
    tag = db.get(Tag, tag_id)

    if tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")

    db.delete(tag)
    db.commit()


@router.post("/recipes/{recipe_id}/tags/{tag_id}", status_code=204)
def assign_tag_to_recipe(
    recipe_id: int,
    tag_id: int,
    db: Session = Depends(get_db)
):
    recipe = db.get(Recipe, recipe_id)
    if recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")

    tag = db.get(Tag, tag_id)
    if tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")

    if tag in recipe.tags:
        raise HTTPException(status_code=409, detail="Tag already assigned to recipe")

    recipe.tags.append(tag)
    db.commit()


@router.get("/recipes/{recipe_id}/tags", response_model=list[TagResponse])
def get_recipe_tags(recipe_id: int, db: Session = Depends(get_db)):
    recipe = db.get(Recipe, recipe_id)

    if recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")

    return recipe.tags


@router.delete("/recipes/{recipe_id}/tags/{tag_id}", status_code=204)
def remove_tag_from_recipe(
    recipe_id: int,
    tag_id: int,
    db: Session = Depends(get_db)
):
    recipe = db.get(Recipe, recipe_id)
    if recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")

    tag = db.get(Tag, tag_id)
    if tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")

    if tag not in recipe.tags:
        raise HTTPException(
            status_code=404,
            detail="Tag not assigned to recipe"
        )

    recipe.tags.remove(tag)
    db.commit()
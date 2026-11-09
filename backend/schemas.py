from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class RecipeCreate(BaseModel):
    name: str
    difficulty: str | None = None
    description: str | None = None
    prep_time: int | None = None
    cook_time: int | None = None
    servings: int | None = None
    calories: Decimal | None = None
    protein: Decimal | None = None
    carbs: Decimal | None = None
    fat: Decimal | None = None
    fibre: Decimal | None = None
    saturates: Decimal | None = None
    salt: Decimal | None = None


class RecipeUpdate(BaseModel):
    name: str | None = None
    difficulty: str | None = None
    description: str | None = None
    prep_time: int | None = None
    cook_time: int | None = None
    servings: int | None = None
    calories: Decimal | None = None
    protein: Decimal | None = None
    carbs: Decimal | None = None
    fat: Decimal | None = None
    fibre: Decimal | None = None
    saturates: Decimal | None = None
    salt: Decimal | None = None


class RecipeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    difficulty: str | None
    description: str | None
    prep_time: int | None
    cook_time: int | None
    servings: int | None
    calories: Decimal | None
    protein: Decimal | None
    carbs: Decimal | None
    fat: Decimal | None
    fibre: Decimal | None
    saturates: Decimal | None
    salt: Decimal | None

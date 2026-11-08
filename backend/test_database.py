from decimal import Decimal

import pytest
from models import (
    Rating,
    Recipe,
    RecipeIngredient,
    RecipeStep,
    RecipeTag,
    Tag,
)
from sqlalchemy.exc import IntegrityError

# --------------------------------------------------
# Database connection test
# --------------------------------------------------

def test_database_connection(db_session):
    assert db_session.is_active


# --------------------------------------------------
# Recipe tests
# --------------------------------------------------

def test_create_recipe(db_session):
    recipe = Recipe(name="Beef Stew")

    db_session.add(recipe)
    db_session.flush()

    assert recipe.id is not None
    assert recipe.name == "Beef Stew"


def test_recipe_name_required(db_session):
    with pytest.raises(IntegrityError):
        db_session.add(Recipe(name=None))
        db_session.flush()


# --------------------------------------------------
# Recipe ingredient tests
# --------------------------------------------------

def test_create_recipe_ingredient(db_session):
    recipe = Recipe(name="Beef Stew")
    ingredient = RecipeIngredient(
        ingredient_name="Beef",
        quantity=Decimal(500),
        unit="g",
        recipe=recipe,
    )

    db_session.add(ingredient)
    db_session.flush()

    assert ingredient.id is not None
    assert ingredient.recipe_id == recipe.id


def test_ingredient_name_required(db_session):
    recipe = Recipe(name="Beef Stew")
    db_session.add(recipe)
    db_session.flush()

    with pytest.raises(IntegrityError):
        db_session.add(
            RecipeIngredient(
                recipe_id=recipe.id,
                ingredient_name=None,
            )
        )
        db_session.flush()


def test_ingredient_recipe_required(db_session):
    with pytest.raises(IntegrityError):
        db_session.add(
            RecipeIngredient(
                ingredient_name="Beef",
                recipe_id=None,
            )
        )
        db_session.flush()


# --------------------------------------------------
# Recipe step tests
# --------------------------------------------------

def test_create_recipe_step(db_session):
    recipe = Recipe(name="Beef Stew")
    step = RecipeStep(
        recipe=recipe,
        step_number=1,
        instruction="Brown the beef.",
    )

    db_session.add(step)
    db_session.flush()

    assert step.id is not None
    assert step.recipe_id == recipe.id


def test_step_number_unique_per_recipe(db_session):
    recipe = Recipe(name="Beef Stew")
    db_session.add(recipe)
    db_session.flush()

    first_step = RecipeStep(
        recipe_id=recipe.id,
        step_number=1,
        instruction="Brown the beef.",
    )
    db_session.add(first_step)
    db_session.flush()

    with pytest.raises(IntegrityError):
        db_session.add(
            RecipeStep(
                recipe_id=recipe.id,
                step_number=1,
                instruction="Add the stock.",
            )
        )
        db_session.flush()


def test_step_instruction_required(db_session):
    recipe = Recipe(name="Beef Stew")
    db_session.add(recipe)
    db_session.flush()

    with pytest.raises(IntegrityError):
        db_session.add(
            RecipeStep(
                recipe_id=recipe.id,
                step_number=1,
                instruction=None,
            )
        )
        db_session.flush()


# --------------------------------------------------
# Tag tests
# --------------------------------------------------

def test_tag_name_unique(db_session):
    db_session.add(Tag(name="Vegetarian"))
    db_session.flush()

    with pytest.raises(IntegrityError):
        db_session.add(Tag(name="Vegetarian"))
        db_session.flush()


# --------------------------------------------------
# Recipe tag tests
# --------------------------------------------------

def test_recipe_tag_pair_unique(db_session):
    recipe = Recipe(name="Beef Stew")
    tag = Tag(name="Dinner")

    db_session.add_all([recipe, tag])
    db_session.flush()

    db_session.add(
        RecipeTag(recipe_id=recipe.id, tag_id=tag.id)
    )
    db_session.flush()

    with pytest.raises(IntegrityError):
        db_session.add(
            RecipeTag(recipe_id=recipe.id, tag_id=tag.id)
        )
        db_session.flush()


# --------------------------------------------------
# Rating tests
# --------------------------------------------------

def test_create_rating(db_session):
    recipe = Recipe(name="Beef Stew")
    rating = Rating(recipe=recipe, rating=5)

    db_session.add(rating)
    db_session.flush()

    assert rating.id is not None
    assert rating.rating == 5


@pytest.mark.parametrize("invalid_rating", [0, 6, -1])
def test_rating_must_be_between_one_and_five(db_session, invalid_rating):
    recipe = Recipe(name="Beef Stew")
    db_session.add(recipe)
    db_session.flush()

    with pytest.raises(IntegrityError):
        db_session.add(
            Rating(
                recipe_id=recipe.id,
                rating=invalid_rating,
            )
        )
        db_session.flush()


def test_only_one_rating_per_recipe(db_session):
    recipe = Recipe(name="Beef Stew")
    db_session.add(recipe)
    db_session.flush()

    db_session.add(Rating(recipe_id=recipe.id, rating=5))
    db_session.flush()

    with pytest.raises(IntegrityError):
        db_session.add(
            Rating(recipe_id=recipe.id, rating=4)
        )
        db_session.flush()


# --------------------------------------------------
# Foreign key tests
# --------------------------------------------------

def test_ingredient_requires_existing_recipe(db_session):
    with pytest.raises(IntegrityError):
        db_session.add(
            RecipeIngredient(
                recipe_id=999999,
                ingredient_name="Beef",
            )
        )
        db_session.flush()


def test_step_requires_existing_recipe(db_session):
    with pytest.raises(IntegrityError):
        db_session.add(
            RecipeStep(
                recipe_id=999999,
                step_number=1,
                instruction="Brown the beef.",
            )
        )
        db_session.flush()


def test_rating_requires_existing_recipe(db_session):
    with pytest.raises(IntegrityError):
        db_session.add(
            Rating(recipe_id=999999, rating=5)
        )
        db_session.flush()


# --------------------------------------------------
# Relationship tests
# --------------------------------------------------

def test_recipe_relationships(db_session):
    recipe = Recipe(name="Beef Stew")

    ingredient = RecipeIngredient(
        ingredient_name="Beef",
        quantity=Decimal(500),
        unit="g",
    )

    step = RecipeStep(
        step_number=1,
        instruction="Brown the beef.",
    )

    tag = Tag(name="Dinner")
    rating = Rating(rating=5)

    recipe.ingredients.append(ingredient)
    recipe.steps.append(step)
    recipe.tags.append(tag)
    recipe.rating = rating

    db_session.add(recipe)
    db_session.flush()

    assert recipe.ingredients[0].ingredient_name == "Beef"
    assert recipe.steps[0].instruction == "Brown the beef."
    assert recipe.tags[0].name == "Dinner"
    assert recipe.rating.rating == 5

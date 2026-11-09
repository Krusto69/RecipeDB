from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    TIMESTAMP,
    CheckConstraint,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.database import Base


class Recipe(Base):
    __tablename__ = "recipes"

    # mapped_column() defines a database column.
    # Mapped[] provides the Python type annotation used by SQLAlchemy.
    # Nullable fields use | None to indicate that they can contain NULL.
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    difficulty: Mapped[str | None] = mapped_column(String(50), nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    prep_time: Mapped[int | None] = mapped_column(Integer, nullable=True)
    cook_time: Mapped[int | None] = mapped_column(Integer, nullable=True)
    servings: Mapped[int | None] = mapped_column(Integer, nullable=True)
    calories: Mapped[Decimal | None] = mapped_column(Numeric, nullable=True)
    protein: Mapped[Decimal | None] = mapped_column(Numeric, nullable=True)
    carbs: Mapped[Decimal | None] = mapped_column(Numeric, nullable=True)
    fat: Mapped[Decimal | None] = mapped_column(Numeric, nullable=True)
    fibre: Mapped[Decimal | None] = mapped_column(Numeric, nullable=True)
    saturates: Mapped[Decimal | None] = mapped_column(Numeric, nullable=True)
    salt: Mapped[Decimal | None] = mapped_column(Numeric, nullable=True)
    image_path: Mapped[str | None] = mapped_column(Text, nullable=True)

    # server_default is evaluated by PostgreSQL when a record is inserted.
    # onupdate tells SQLAlchemy to update this value when the ORM updates the record.
    # timezone=True uses PostgreSQL's TIMESTAMP WITH TIME ZONE type.
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    # ORM relationships allow us to navigate between related model objects.
    # back_populates connects the relationship to its counterpart on the other model.
    # These are ORM relationships, not additional database columns.
    ingredients: Mapped[list["RecipeIngredient"]] = relationship(
        back_populates="recipe"
    )

    steps: Mapped[list["RecipeStep"]] = relationship(
        back_populates="recipe"
    )

    # A recipe has one rating in v1, so this is a single object rather than a list.
    rating: Mapped["Rating | None"] = relationship(
        back_populates="recipe"
    )

    # secondary specifies the junction table used for the many-to-many relationship.
    tags: Mapped[list["Tag"]] = relationship(
        secondary="recipe_tags",
        back_populates="recipes"
    )


class RecipeIngredient(Base):
    __tablename__ = "recipe_ingredients"

    id: Mapped[int] = mapped_column(primary_key=True)

    # ForeignKey links this ingredient to its parent recipe.
    # Multiple ingredients can reference the same recipe.
    recipe_id: Mapped[int] = mapped_column(
        ForeignKey("recipes.id"),
        nullable=False
    )

    ingredient_name: Mapped[str] = mapped_column(String(255), nullable=False)
    quantity: Mapped[Decimal | None] = mapped_column(Numeric, nullable=True)
    unit: Mapped[str | None] = mapped_column(String(50), nullable=True)

    recipe: Mapped["Recipe"] = relationship(
        back_populates="ingredients"
    )


class RecipeStep(Base):
    __tablename__ = "recipe_steps"

    # Table-level constraint: step_number must be unique within each recipe.
    # This allows different recipes to have a step 1, but prevents duplicates within the same recipe.
    __table_args__ = (
        UniqueConstraint("recipe_id", "step_number", name="unique_recipe_step_number"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    recipe_id: Mapped[int] = mapped_column(
        ForeignKey("recipes.id"),
        nullable=False
    )

    step_number: Mapped[int] = mapped_column(Integer, nullable=False)
    instruction: Mapped[str] = mapped_column(Text, nullable=False)

    recipe: Mapped["Recipe"] = relationship(
        back_populates="steps"
    )


class Tag(Base):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)

    recipes: Mapped[list["Recipe"]] = relationship(
        secondary="recipe_tags",
        back_populates="tags"
    )


class RecipeTag(Base):
    __tablename__ = "recipe_tags"

    # Composite primary key: the combination of recipe_id and tag_id must be unique.
    # This prevents the same tag from being assigned to a recipe more than once.
    recipe_id: Mapped[int] = mapped_column(
        ForeignKey("recipes.id"),
        primary_key=True
    )

    tag_id: Mapped[int] = mapped_column(
        ForeignKey("tags.id"),
        primary_key=True
    )


class Rating(Base):
    __tablename__ = "ratings"

    # Database-level constraint ensures ratings are always between 1 and 5.
    __table_args__ = (
        CheckConstraint("rating BETWEEN 1 AND 5"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    # unique=True enforces one rating per recipe in v1.
    # This will need to change when we introduce multiple users in v2.
    recipe_id: Mapped[int] = mapped_column(
        ForeignKey("recipes.id"),
        nullable=False,
        unique=True
    )

    rating: Mapped[int] = mapped_column(Integer, nullable=False)
    comment: Mapped[str | None] = mapped_column(Text, nullable=True)

    recipe: Mapped["Recipe"] = relationship(
        back_populates="rating"
    )

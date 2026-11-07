# Database Design Document for RecipeDB(TDB)

This document will contain the database design for the RecipeDB product that will store all of the data required, including:

- Recipe data

## What tables does the database need?

- Recipe table for storing all the recipes.
- Recipe Ingredients table for storing the ingredients for each recipe. This requires it's own table because of the one-many relationship it has with the recipe table.
- Recipe Ratings table, for storing all the ratings for each recipe (This doesn't make sense for version one as it is single-user and there will only be one recipe, however I will create this table now in preperation for version 2.0 where each recipe will have multiple ratings)
- Recipe Steps for storing each step of the recipe. This table is required because it has a one-many relationship with the recipe table.
- Tags table for storing all the different unique tags that are given to different recipes.
- Recipe Tags. This table is required for linking together the tags table and the recipe table as they have a many-many relationship where one recipe may have multiple tags and one tag may have multiple recipes.

## What data do I need to store?

Here I will list all the individual data points that need to be stored in their respective tables.

### Recipe Table

| Field | Data Type | Description | Contraints |
| ------------- | --------- | ----------------------------------------- |
| `id` | INTEGER | Unique recipe identifier | PRIMARY KEY |
| `name` | VARCHAR | Recipe name | NOT NULL |
| `Difficulty` | VARCHAR | User defined recipe difficulty | NULL |
| `description` | TEXT | Optional recipe description | NULL |
| `prep_time` | INTEGER | Preparation time in minutes | NULL |
| `cook_time` | INTEGER | Cooking time in minutes | NULL |
| `servings` | INTEGER | Number of servings | NULL |
| `calories` | DECIMAL | Calories per serving | NULL |
| `protein` | DECIMAL | Protein per serving | NULL |
| `carbs` | DECIMAL | Carbohydrates per serving | NULL |
| `fat` | DECIMAL | Fat per serving | NULL |
| `fibre` | DECIMAL | Fibre per serving | NULL |
| `saturates` | DECIMAL | saturates per serving | NULL |
| `salt` | DECIMAL | salt per serving | NULL |
| `image_path` | TEXT | Location of the recipe photograph | NULL |
| `created_at` | TIMESTAMP | Date and time the recipe was created | NOT NULL |
| `updated_at` | TIMESTAMP | Date and time the recipe was last updated | NOT NULL |

### Ingredients Table

| Field | Data Type | Description | Constraints |
|---|---|---|---|
| `id` | INTEGER | Unique ingredient record identifier | PRIMARY KEY |
| `recipe_id` | INTEGER | References the associated recipe | FOREIGN KEY, NOT NULL |
| `ingredient_name` | VARCHAR | Name of the ingredient | NOT NULL |
| `quantity` | DECIMAL | Ingredient quantity | NULL |
| `unit` | VARCHAR | Unit of measurement | NULL |

### Recipe Steps Table

| Field | Data Type | Description | Constraints |
|---|---|---|---|
| `id` | INTEGER | Unique step identifier | PRIMARY KEY |
| `recipe_id` | INTEGER | References the associated recipe | FOREIGN KEY, NOT NULL |
| `step_number` | INTEGER | Position of the instruction in the recipe | NOT NULL |
| `instruction` | TEXT | The instruction for this step | NOT NULL |

step number will be UNIQUE for the recipe_id FOREIGN KEY so that e.g. recipe id 1 can only have 1 step 1.

### Tags

| Field | Data Type | Description | Constraints |
|---|---|---|---|
| `id` | INTEGER | Unique tag identifier | PRIMARY KEY |
| `name` | VARCHAR | Name of the tag | NOT NULL, UNIQUE |

### Recipe tags

| Field | Data Type | Description | Constraints |
|---|---|---|---|
| `recipe_id` | INTEGER | References the associated recipe | FOREIGN KEY, NOT NULL |
| `tag_id` | INTEGER | References the associated tag | FOREIGN KEY, NOT NULL |

Another constraint addes to the table will be that the same tag will no be able to be added to a recipe more than once.

### Ratings Table

| Field | Data Type | Description | Constraints |
|---|---|---|---|
| `id` | INTEGER | Unique rating identifier | PRIMARY KEY |
| `recipe_id` | INTEGER | References the associated recipe | FOREIGN KEY, NOT NULL, UNIQUE |
| `rating` | INTEGER | Recipe rating (1–5) | NOT NULL |
| `comment` | TEXT | Optional written review | NULL |

Ratings will be restricted from the values of 1 to 5.

## Entity Relationship Diagram

![RecipeDB Entity Relationship Diagram](images/ERD.png) - Made using dbdiagram.io


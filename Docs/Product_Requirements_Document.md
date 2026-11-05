# Product Requirements Document (PRD)

## What is the Product Requirements Document?

This document defines the requirements and specifications for RecipeDB, initially focusing on Version 1.0 of the application.

It will serve as the primary reference throughout the development process, outlining the product's intended functionality, features, scope and objectives.

Although the initial focus is Version 1.0, this document is intended to evolve alongside the project and may be expanded to accommodate future versions and additional functionality.

## What is RecipeDB(TBD)?

RecipeDB is a web-based recipe management application designed to provide a centralised location for storing, organising and managing recipes. Each recipe is stored in a structured format, containing information such as ingredients, quantities, preparation instructions, nutritional values and other relevant attributes. The application will allow users to browse, search, filter and sort their recipe collection based on these attributes, making it easier to find recipes that meet specific requirements and preferences. Initially developed as a single-user application for personal use, RecipeDB will be designed with the potential to expand into a multi-user platform with additional functionality in future versions.

## Product Scope

### Version 1

RecipeDB 1.0 will be a single-user web application designed for personal recipe management. Users will be able to create, view, edit and delete recipes through a standardised interface. Recipes will contain structured ingredient information, preparation instructions, nutritional values, tags and a photograph. Users will also be able to search, filter and sort their recipe collection using various recipe attributes.

### Not in version 1

- User registration and authentication.
- Multiple user accounts.
- Importing recipes from external websites.
- Customisable recipe layouts.
- Automatic nutritional calculations.
- Meal planning and shopping list generation.
- Global Recipe Discovery(multi-user-functionality).

All the exclusions from version 1 listed will be implemented in future versions of the product.

## Mimimum Viable Product (MVP) Requirements

The following features define the minimum functionality required for the initial release of RecipeDB.

## Recipe Management

- Create new recipes using a standardised form.
- View individual recipes and their details.
- Edit existing recipes.
- Delete recipes.
- Allow the user to assign a personal rating to each recipe using a 1–5 star rating system.
- Allow the user to update or remove an existing rating.
- Store ratings alongside their associated recipes.

## Recipe Data

- Store recipe names and descriptions.
- Store preparation time, cooking time and serving quantities.
- Store ingredients with individual quantities and units of measurement.
- Store recipe instructions as individual steps.
- Store nutritional information per serving.
- Assign multiple user-defined tags to recipes.
- Upload one photograph per recipe.

## Recipe Dicovery

- Search recipes by name.
- Filter recipes using tags and other recipe attributes.
- Sort recipes using selected attributes, including preparation time, cooking time and nutritional values.

## Data Persistence

- Store recipes and associated information in a database.
- Ensure recipe information remains available between application sessions.

## Functional Requirements

### Recipe Creation

A user must be able to create and save a new recipe using a standardised form.

The form should allow the user to enter:

- Recipe name (mandatory)
- Description
- Preparation time
- Cooking time
- Number of servings
- Ingredients (name, quantity and unit)
- Cooking instructions (individual steps)
- Nutritional information (per serving)
- Tags
- Recipe photograph

Only the recipe name is required. All other fields are optional and can be completed or updated later.

## Recipe Viewing

- A user must be able to view an individual recipe and its associated information.
- The recipe page should display all available information, including:
- Recipe name and description
- Preparation time, cooking time and number of servings
- Ingredients, including quantities and units
- Cooking instructions, displayed as individual steps
- Nutritional information per serving
- Assigned tags
- Recipe photograph
- Personal rating

## Recipe Editing and Deletion

- A user must be able to edit and update any information associated with an existing recipe.
- A user must also be able to delete an existing recipe from the database.
- Before deleting a recipe, the application should request confirmation to prevent accidental deletion.

## Recipe Ratings

- A user must be able to assign a personal rating to each recipe using a 1–5 star rating system.
- The user must be able to update or remove an existing rating.
- Each recipe can have a maximum of one rating, which is stored alongside the associated recipe.

## Database and Data Management

The database must:

- Store all recipe information and associated data, including ingredients, instructions, tags, photographs and personal ratings.
- Maintain relationships between recipes and their associated data.
- Support querying, filtering and sorting recipes using their stored attributes.
- Allow recipe information to be created, updated and deleted.
- Ensure data persists between application sessions.

## Recipe Discovery

A user must be able to find recipes within their collection using search, filtering and sorting functionality.

- Search: Search recipes by name.
- Filtering: Filter recipes using available attributes, such as tags, preparation time, cooking time and nutritional values.
- Sorting: Sort recipes by selected attributes, such as name, preparation time, cooking time and nutritional values.

## Non-Functional Requirements

### Performance

The application should respond quickly to user interactions, including loading recipes, searching, filtering and sorting.

### Usability

The application should have an intuitive and straightforward interface, making it easy to create, manage and find recipes without unnecessary complexity.

### Reliability

The application should consistently function as expected and ensure that recipe data is stored correctly and remains available between sessions.

### Security

The application should protect stored recipe data and prevent unauthorised access or modification.

## Future Features

The following features are outside the scope of version 1.0 but may be considered for future releases.

- **User Accounts:** Registration, authentication and support for multiple users.
- **Global Recipe Ratings:** Allow users to rate recipes and display aggregated ratings from multiple users.
- **Recipe Importing:** Import recipes from external websites rather than requiring manual entry.
- **Customisable Recipe Layouts:** Allow users to choose from different layouts when creating and displaying recipes.
- **Automatic Nutritional Calculations:** Calculate nutritional values based on recipe ingredients and quantities.
- **Meal Planning:** Allow users to plan meals using recipes from their collection.
- **Shopping Lists:** Generate shopping lists based on selected recipes.
- **Print function** Print the recipe.
- **Recomendations** Recomend recipes based on ratings and potentially user preference based on user data.
- **Alternative recipes** Suggest alternative recipes based on the current recipe being viewed and their respective ratings.

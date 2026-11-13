def test_create_ingredient(client):
    recipe_response = client.post("/recipes", json={"name": "Pancakes"})
    recipe_id = recipe_response.json()["id"]

    response = client.post(
        f"/recipes/{recipe_id}/ingredients",
        json={
            "ingredient_name": "Flour",
            "quantity": 200,
            "unit": "g"
        }
    )

    assert response.status_code == 201
    data = response.json()
    assert data["ingredient_name"] == "Flour"
    assert data["quantity"] == "200"
    assert data["unit"] == "g"
    assert data["id"] is not None


def test_get_ingredients(client):
    recipe_response = client.post("/recipes", json={"name": "Pancakes"})
    recipe_id = recipe_response.json()["id"]

    client.post(
        f"/recipes/{recipe_id}/ingredients",
        json={"ingredient_name": "Flour", "quantity": 200, "unit": "g"}
    )
    client.post(
        f"/recipes/{recipe_id}/ingredients",
        json={"ingredient_name": "Milk", "quantity": 300, "unit": "ml"}
    )

    response = client.get(f"/recipes/{recipe_id}/ingredients")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["ingredient_name"] == "Flour"
    assert data[1]["ingredient_name"] == "Milk"


def test_update_ingredient(client):
    recipe_response = client.post("/recipes", json={"name": "Pancakes"})
    recipe_id = recipe_response.json()["id"]

    ingredient_response = client.post(
        f"/recipes/{recipe_id}/ingredients",
        json={"ingredient_name": "Flour", "quantity": 200, "unit": "g"}
    )
    ingredient_id = ingredient_response.json()["id"]

    response = client.put(
        f"/recipes/{recipe_id}/ingredients/{ingredient_id}",
        json={"quantity": 250}
    )

    assert response.status_code == 200
    assert response.json()["quantity"] == "250"
    assert response.json()["ingredient_name"] == "Flour"


def test_delete_ingredient(client):
    recipe_response = client.post("/recipes", json={"name": "Pancakes"})
    recipe_id = recipe_response.json()["id"]

    ingredient_response = client.post(
        f"/recipes/{recipe_id}/ingredients",
        json={"ingredient_name": "Flour", "quantity": 200, "unit": "g"}
    )
    ingredient_id = ingredient_response.json()["id"]

    response = client.delete(
        f"/recipes/{recipe_id}/ingredients/{ingredient_id}"
    )

    assert response.status_code == 204

    get_response = client.get(f"/recipes/{recipe_id}/ingredients")
    assert get_response.json() == []

def test_create_ingredient_recipe_not_found(client):
    response = client.post(
        "/recipes/-1/ingredients",
        json={"ingredient_name": "Flour", "quantity": 200, "unit": "g"}
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Recipe not found"


def test_get_ingredients_recipe_not_found(client):
    response = client.get("/recipes/-1/ingredients")

    assert response.status_code == 404
    assert response.json()["detail"] == "Recipe not found"


def test_update_ingredient_not_found(client):
    recipe_response = client.post("/recipes", json={"name": "Pancakes"})
    recipe_id = recipe_response.json()["id"]

    response = client.put(
        f"/recipes/{recipe_id}/ingredients/-1",
        json={"quantity": 200}
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Ingredient not found"


def test_delete_ingredient_not_found(client):
    recipe_response = client.post("/recipes", json={"name": "Pancakes"})
    recipe_id = recipe_response.json()["id"]

    response = client.delete(
        f"/recipes/{recipe_id}/ingredients/-1"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Ingredient not found"


def test_update_ingredient_wrong_recipe(client):
    recipe1_response = client.post("/recipes", json={"name": "Pancakes"})
    recipe1_id = recipe1_response.json()["id"]

    recipe2_response = client.post("/recipes", json={"name": "Pizza"})
    recipe2_id = recipe2_response.json()["id"]

    ingredient_response = client.post(
        f"/recipes/{recipe1_id}/ingredients",
        json={"ingredient_name": "Flour", "quantity": 200, "unit": "g"}
    )
    ingredient_id = ingredient_response.json()["id"]

    response = client.put(
        f"/recipes/{recipe2_id}/ingredients/{ingredient_id}",
        json={"quantity": 300}
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Ingredient not found"


def test_delete_ingredient_wrong_recipe(client):
    recipe1_response = client.post("/recipes", json={"name": "Pancakes"})
    recipe1_id = recipe1_response.json()["id"]

    recipe2_response = client.post("/recipes", json={"name": "Pizza"})
    recipe2_id = recipe2_response.json()["id"]

    ingredient_response = client.post(
        f"/recipes/{recipe1_id}/ingredients",
        json={"ingredient_name": "Flour", "quantity": 200, "unit": "g"}
    )
    ingredient_id = ingredient_response.json()["id"]

    response = client.delete(
        f"/recipes/{recipe2_id}/ingredients/{ingredient_id}"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Ingredient not found"
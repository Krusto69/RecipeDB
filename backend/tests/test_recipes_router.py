# testing CRUD for the recipes router

def test_create_recipe(client):
    response = client.post(
        "/recipes",
        json={"name": "Pancakes"}
    )

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == "Pancakes"
    assert data["id"] is not None


def test_get_recipes(client):
    client.post("/recipes", json={"name": "Pancakes"})
    client.post("/recipes", json={"name": "Pizza"})

    response = client.get("/recipes")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2
    assert data[0]["name"] == "Pancakes"
    assert data[1]["name"] == "Pizza"    


def test_get_recipe(client):
    create_response = client.post(
        "/recipes",
        json={"name": "Pancakes"}
    )

    recipe_id = create_response.json()["id"]

    response = client.get(f"/recipes/{recipe_id}")

    assert response.status_code == 200
    assert response.json()["id"] == recipe_id
    assert response.json()["name"] == "Pancakes"


def test_get_recipe_not_found(client):
    response = client.get("/recipes/-1")

    assert response.status_code == 404
    assert response.json()["detail"] == "Recipe not found"


def test_update_recipe(client):
    create_response = client.post(
        "/recipes",
        json={"name": "Pancakes"}
    )

    recipe_id = create_response.json()["id"]

    response = client.put(
        f"/recipes/{recipe_id}",
        json={"name": "American Pancakes"}
    )

    assert response.status_code == 200
    assert response.json()["name"] == "American Pancakes"


def test_update_recipe_not_found(client):
    response = client.put(
        "/recipes/-1",
        json={"name": "American Pancakes"}
    )

    assert response.status_code == 404


def test_delete_recipe(client):
    create_response = client.post(
        "/recipes",
        json={"name": "Pancakes"}
    )

    recipe_id = create_response.json()["id"]

    response = client.delete(f"/recipes/{recipe_id}")

    assert response.status_code == 204

    get_response = client.get(f"/recipes/{recipe_id}")

    assert get_response.status_code == 404



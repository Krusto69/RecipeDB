from backend.models import Recipe


def test_create_tag(client):
    response = client.post("/tags", json={"name": "Vegetarian"})

    assert response.status_code == 201

    data = response.json()
    assert data["name"] == "Vegetarian"
    assert data["id"] is not None


def test_get_tags(client):
    client.post("/tags", json={"name": "Vegetarian"})
    client.post("/tags", json={"name": "Dessert"})

    response = client.get("/tags")

    assert response.status_code == 200

    data = response.json()
    assert len(data) == 2
    assert {tag["name"] for tag in data} == {"Vegetarian", "Dessert"}


def test_get_tag(client):
    create_response = client.post("/tags", json={"name": "Vegetarian"})
    tag_id = create_response.json()["id"]

    response = client.get(f"/tags/{tag_id}")

    assert response.status_code == 200
    assert response.json()["id"] == tag_id
    assert response.json()["name"] == "Vegetarian"


def test_update_tag(client):
    create_response = client.post("/tags", json={"name": "Vegetarian"})
    tag_id = create_response.json()["id"]

    response = client.put(
        f"/tags/{tag_id}",
        json={"name": "Vegan"}
    )

    assert response.status_code == 200
    assert response.json()["name"] == "Vegan"


def test_delete_tag(client):
    create_response = client.post("/tags", json={"name": "Vegetarian"})
    tag_id = create_response.json()["id"]

    response = client.delete(f"/tags/{tag_id}")

    assert response.status_code == 204

    get_response = client.get(f"/tags/{tag_id}")
    assert get_response.status_code == 404


def test_create_duplicate_tag(client):
    client.post("/tags", json={"name": "Vegetarian"})

    response = client.post("/tags", json={"name": "Vegetarian"})

    assert response.status_code == 409
    assert response.json()["detail"] == "Tag already exists"


def test_update_tag_duplicate_name(client):
    client.post("/tags", json={"name": "Vegetarian"})

    tag_response = client.post("/tags", json={"name": "Dessert"})
    tag_id = tag_response.json()["id"]

    response = client.put(
        f"/tags/{tag_id}",
        json={"name": "Vegetarian"}
    )

    assert response.status_code == 409
    assert response.json()["detail"] == "Tag name already exists"


def test_get_tag_not_found(client):
    response = client.get("/tags/-1")

    assert response.status_code == 404
    assert response.json()["detail"] == "Tag not found"


def test_update_tag_not_found(client):
    response = client.put(
        "/tags/-1",
        json={"name": "Vegetarian"}
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Tag not found"


def test_delete_tag_not_found(client):
    response = client.delete("/tags/-1")

    assert response.status_code == 404
    assert response.json()["detail"] == "Tag not found"


def test_assign_tag_to_recipe(client):
    recipe_response = client.post(
        "/recipes",
        json={"name": "Vegetarian Curry"}
    )
    recipe_id = recipe_response.json()["id"]

    tag_response = client.post(
        "/tags",
        json={"name": "Vegetarian"}
    )
    tag_id = tag_response.json()["id"]

    response = client.post(f"/recipes/{recipe_id}/tags/{tag_id}")

    assert response.status_code == 204


def test_assign_tag_to_nonexistent_recipe(client):
    tag_response = client.post(
        "/tags",
        json={"name": "Vegetarian"}
    )
    tag_id = tag_response.json()["id"]

    response = client.post(f"/recipes/-1/tags/{tag_id}")

    assert response.status_code == 404
    assert response.json()["detail"] == "Recipe not found"


def test_assign_nonexistent_tag_to_recipe(client):
    recipe_response = client.post(
        "/recipes",
        json={"name": "Vegetarian Curry"}
    )
    recipe_id = recipe_response.json()["id"]

    response = client.post(f"/recipes/{recipe_id}/tags/-1")

    assert response.status_code == 404
    assert response.json()["detail"] == "Tag not found"


def test_assign_duplicate_tag_to_recipe(client):
    recipe_response = client.post(
        "/recipes",
        json={"name": "Vegetarian Curry"}
    )
    recipe_id = recipe_response.json()["id"]

    tag_response = client.post(
        "/tags",
        json={"name": "Vegetarian"}
    )
    tag_id = tag_response.json()["id"]

    client.post(f"/recipes/{recipe_id}/tags/{tag_id}")

    response = client.post(f"/recipes/{recipe_id}/tags/{tag_id}")

    assert response.status_code == 409
    assert response.json()["detail"] == "Tag already assigned to recipe"


def test_assign_tag_creates_relationship(client, db_session):
    recipe_response = client.post(
        "/recipes",
        json={"name": "Vegetarian Curry"}
    )
    recipe_id = recipe_response.json()["id"]

    tag_response = client.post(
        "/tags",
        json={"name": "Vegetarian"}
    )
    tag_id = tag_response.json()["id"]

    client.post(f"/recipes/{recipe_id}/tags/{tag_id}")

    recipe = db_session.get(Recipe, recipe_id)

    assert len(recipe.tags) == 1
    assert recipe.tags[0].name == "Vegetarian"


def test_get_recipe_tags(client):
    recipe_response = client.post(
        "/recipes",
        json={"name": "Vegetarian Curry"}
    )
    recipe_id = recipe_response.json()["id"]

    tag_response = client.post(
        "/tags",
        json={"name": "Vegetarian"}
    )
    tag_id = tag_response.json()["id"]

    client.post(f"/recipes/{recipe_id}/tags/{tag_id}")

    response = client.get(f"/recipes/{recipe_id}/tags")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["name"] == "Vegetarian"
    assert response.json()[0]["id"] == tag_id


def test_get_recipe_tags_empty(client):
    recipe_response = client.post(
        "/recipes",
        json={"name": "Plain Rice"}
    )
    recipe_id = recipe_response.json()["id"]

    response = client.get(f"/recipes/{recipe_id}/tags")

    assert response.status_code == 200
    assert response.json() == []


def test_get_recipe_tags_not_found(client):
    response = client.get("/recipes/-1/tags")

    assert response.status_code == 404
    assert response.json()["detail"] == "Recipe not found"


def test_remove_tag_from_recipe(client):
    recipe_response = client.post(
        "/recipes",
        json={"name": "Vegetarian Curry"}
    )
    recipe_id = recipe_response.json()["id"]

    tag_response = client.post(
        "/tags",
        json={"name": "Vegetarian"}
    )
    tag_id = tag_response.json()["id"]

    client.post(f"/recipes/{recipe_id}/tags/{tag_id}")

    response = client.delete(f"/recipes/{recipe_id}/tags/{tag_id}")

    assert response.status_code == 204


def test_remove_tag_preserves_recipe_and_tag(client):
    recipe_response = client.post(
        "/recipes",
        json={"name": "Vegetarian Curry"}
    )
    recipe_id = recipe_response.json()["id"]

    tag_response = client.post(
        "/tags",
        json={"name": "Vegetarian"}
    )
    tag_id = tag_response.json()["id"]

    client.post(f"/recipes/{recipe_id}/tags/{tag_id}")
    client.delete(f"/recipes/{recipe_id}/tags/{tag_id}")

    recipe_check = client.get(f"/recipes/{recipe_id}")
    tag_check = client.get(f"/tags/{tag_id}")

    assert recipe_check.status_code == 200
    assert tag_check.status_code == 200


def test_remove_tag_from_nonexistent_recipe(client):
    tag_response = client.post(
        "/tags",
        json={"name": "Vegetarian"}
    )
    tag_id = tag_response.json()["id"]

    response = client.delete(f"/recipes/-1/tags/{tag_id}")

    assert response.status_code == 404
    assert response.json()["detail"] == "Recipe not found"


def test_remove_nonexistent_tag_from_recipe(client):
    recipe_response = client.post(
        "/recipes",
        json={"name": "Vegetarian Curry"}
    )
    recipe_id = recipe_response.json()["id"]

    response = client.delete(f"/recipes/{recipe_id}/tags/-1")

    assert response.status_code == 404
    assert response.json()["detail"] == "Tag not found"


def test_remove_unassigned_tag_from_recipe(client):
    recipe_response = client.post(
        "/recipes",
        json={"name": "Vegetarian Curry"}
    )
    recipe_id = recipe_response.json()["id"]

    tag_response = client.post(
        "/tags",
        json={"name": "Vegetarian"}
    )
    tag_id = tag_response.json()["id"]

    response = client.delete(f"/recipes/{recipe_id}/tags/{tag_id}")

    assert response.status_code == 404
    assert response.json()["detail"] == "Tag not assigned to recipe"


def test_delete_tag_cascades_recipe_tags(client, db_session):
    recipe_response = client.post(
        "/recipes",
        json={"name": "Vegetarian Curry"}
    )
    recipe_id = recipe_response.json()["id"]

    tag_response = client.post(
        "/tags",
        json={"name": "Vegetarian"}
    )
    tag_id = tag_response.json()["id"]

    client.post(f"/recipes/{recipe_id}/tags/{tag_id}")

    response = client.delete(f"/tags/{tag_id}")

    assert response.status_code == 204

    recipe = db_session.get(Recipe, recipe_id)

    assert recipe is not None
    assert recipe.tags == []
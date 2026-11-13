def test_create_step(client):
    recipe_response = client.post("/recipes", json={"name": "Pancakes"})
    recipe_id = recipe_response.json()["id"]

    response = client.post(
        f"/recipes/{recipe_id}/steps",
        json={
            "step_number": 1,
            "instruction": "Mix the ingredients"
        }
    )

    assert response.status_code == 201
    data = response.json()
    assert data["step_number"] == 1
    assert data["instruction"] == "Mix the ingredients"
    assert data["id"] is not None


def test_get_steps(client):
    recipe_response = client.post("/recipes", json={"name": "Pancakes"})
    recipe_id = recipe_response.json()["id"]

    client.post(
        f"/recipes/{recipe_id}/steps",
        json={"step_number": 2, "instruction": "Cook the pancakes"}
    )
    client.post(
        f"/recipes/{recipe_id}/steps",
        json={"step_number": 1, "instruction": "Mix the ingredients"}
    )

    response = client.get(f"/recipes/{recipe_id}/steps")

    assert response.status_code == 200

    data = response.json()
    assert len(data) == 2
    assert data[0]["step_number"] == 1
    assert data[0]["instruction"] == "Mix the ingredients"
    assert data[1]["step_number"] == 2
    assert data[1]["instruction"] == "Cook the pancakes"


def test_update_step(client):
    recipe_response = client.post("/recipes", json={"name": "Pancakes"})
    recipe_id = recipe_response.json()["id"]

    step_response = client.post(
        f"/recipes/{recipe_id}/steps",
        json={"step_number": 1, "instruction": "Mix ingredients"}
    )
    step_id = step_response.json()["id"]

    response = client.put(
        f"/recipes/{recipe_id}/steps/{step_id}",
        json={"instruction": "Mix all ingredients together"}
    )

    assert response.status_code == 200

    data = response.json()
    assert data["step_number"] == 1
    assert data["instruction"] == "Mix all ingredients together"


def test_delete_step(client):
    recipe_response = client.post("/recipes", json={"name": "Pancakes"})
    recipe_id = recipe_response.json()["id"]

    step_response = client.post(
        f"/recipes/{recipe_id}/steps",
        json={"step_number": 1, "instruction": "Mix ingredients"}
    )
    step_id = step_response.json()["id"]

    response = client.delete(
        f"/recipes/{recipe_id}/steps/{step_id}"
    )

    assert response.status_code == 204

    get_response = client.get(f"/recipes/{recipe_id}/steps")
    assert get_response.status_code == 200
    assert get_response.json() == []


def test_create_step_recipe_not_found(client):
    response = client.post(
        "/recipes/-1/steps",
        json={"step_number": 1, "instruction": "Mix ingredients"}
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Recipe not found"


def test_get_steps_recipe_not_found(client):
    response = client.get("/recipes/-1/steps")

    assert response.status_code == 404
    assert response.json()["detail"] == "Recipe not found"


def test_update_step_not_found(client):
    recipe_response = client.post("/recipes", json={"name": "Pancakes"})
    recipe_id = recipe_response.json()["id"]

    response = client.put(
        f"/recipes/{recipe_id}/steps/-1",
        json={"instruction": "Mix ingredients"}
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Step not found"


def test_delete_step_not_found(client):
    recipe_response = client.post("/recipes", json={"name": "Pancakes"})
    recipe_id = recipe_response.json()["id"]

    response = client.delete(
        f"/recipes/{recipe_id}/steps/-1"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Step not found"


def test_update_step_wrong_recipe(client):
    recipe1_response = client.post("/recipes", json={"name": "Pancakes"})
    recipe1_id = recipe1_response.json()["id"]

    recipe2_response = client.post("/recipes", json={"name": "Pizza"})
    recipe2_id = recipe2_response.json()["id"]

    step_response = client.post(
        f"/recipes/{recipe1_id}/steps",
        json={"step_number": 1, "instruction": "Mix ingredients"}
    )
    step_id = step_response.json()["id"]

    response = client.put(
        f"/recipes/{recipe2_id}/steps/{step_id}",
        json={"instruction": "Bake the pizza"}
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Step not found"


def test_delete_step_wrong_recipe(client):
    recipe1_response = client.post("/recipes", json={"name": "Pancakes"})
    recipe1_id = recipe1_response.json()["id"]

    recipe2_response = client.post("/recipes", json={"name": "Pizza"})
    recipe2_id = recipe2_response.json()["id"]

    step_response = client.post(
        f"/recipes/{recipe1_id}/steps",
        json={"step_number": 1, "instruction": "Mix ingredients"}
    )
    step_id = step_response.json()["id"]

    response = client.delete(
        f"/recipes/{recipe2_id}/steps/{step_id}"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Step not found"


def test_create_step_duplicate_step_number(client):
    recipe_response = client.post("/recipes", json={"name": "Pancakes"})
    recipe_id = recipe_response.json()["id"]

    client.post(
        f"/recipes/{recipe_id}/steps",
        json={"step_number": 1, "instruction": "Mix ingredients"}
    )

    response = client.post(
        f"/recipes/{recipe_id}/steps",
        json={"step_number": 1, "instruction": "Cook pancakes"}
    )

    assert response.status_code == 409
    assert response.json()["detail"] == "Step number already exists for this recipe"
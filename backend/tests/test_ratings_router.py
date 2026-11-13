from backend.models import Rating, Recipe


def test_create_rating(client):
    recipe_response = client.post(
        "/recipes",
        json={"name": "Chocolate Cake"}
    )
    recipe_id = recipe_response.json()["id"]

    response = client.post(
        f"/recipes/{recipe_id}/rating",
        json={
            "rating": 5,
            "comment": "Absolutely delicious"
        }
    )

    assert response.status_code == 201
    assert response.json()["rating"] == 5
    assert response.json()["comment"] == "Absolutely delicious"
    assert "id" in response.json()


def test_create_rating_without_comment(client):
    recipe_response = client.post(
        "/recipes",
        json={"name": "Chocolate Cake"}
    )
    recipe_id = recipe_response.json()["id"]

    response = client.post(
        f"/recipes/{recipe_id}/rating",
        json={"rating": 4}
    )

    assert response.status_code == 201
    assert response.json()["rating"] == 4
    assert response.json()["comment"] is None


def test_create_rating_recipe_not_found(client):
    response = client.post(
        "/recipes/-1/rating",
        json={"rating": 5}
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Recipe not found"


def test_create_duplicate_rating(client):
    recipe_response = client.post(
        "/recipes",
        json={"name": "Chocolate Cake"}
    )
    recipe_id = recipe_response.json()["id"]

    client.post(
        f"/recipes/{recipe_id}/rating",
        json={"rating": 5}
    )

    response = client.post(
        f"/recipes/{recipe_id}/rating",
        json={"rating": 4}
    )

    assert response.status_code == 409
    assert response.json()["detail"] == "Recipe already has a rating"


def test_create_rating_invalid_value(client):
    recipe_response = client.post(
        "/recipes",
        json={"name": "Chocolate Cake"}
    )
    recipe_id = recipe_response.json()["id"]

    response = client.post(
        f"/recipes/{recipe_id}/rating",
        json={"rating": 6}
    )

    assert response.status_code == 422


def test_create_rating_below_minimum(client):
    recipe_response = client.post(
        "/recipes",
        json={"name": "Chocolate Cake"}
    )
    recipe_id = recipe_response.json()["id"]

    response = client.post(
        f"/recipes/{recipe_id}/rating",
        json={"rating": 0}
    )

    assert response.status_code == 422


def test_get_rating(client):
    recipe_response = client.post(
        "/recipes",
        json={"name": "Chocolate Cake"}
    )
    recipe_id = recipe_response.json()["id"]

    client.post(
        f"/recipes/{recipe_id}/rating",
        json={
            "rating": 5,
            "comment": "Absolutely delicious"
        }
    )

    response = client.get(f"/recipes/{recipe_id}/rating")

    assert response.status_code == 200
    assert response.json()["rating"] == 5
    assert response.json()["comment"] == "Absolutely delicious"


def test_get_rating_not_found(client):
    recipe_response = client.post(
        "/recipes",
        json={"name": "Chocolate Cake"}
    )
    recipe_id = recipe_response.json()["id"]

    response = client.get(f"/recipes/{recipe_id}/rating")

    assert response.status_code == 404
    assert response.json()["detail"] == "Rating not found"


def test_get_rating_recipe_not_found(client):
    response = client.get("/recipes/-1/rating")

    assert response.status_code == 404
    assert response.json()["detail"] == "Recipe not found"


def test_update_rating(client):
    recipe_response = client.post(
        "/recipes",
        json={"name": "Chocolate Cake"}
    )
    recipe_id = recipe_response.json()["id"]

    client.post(
        f"/recipes/{recipe_id}/rating",
        json={
            "rating": 3,
            "comment": "It was okay"
        }
    )

    response = client.put(
        f"/recipes/{recipe_id}/rating",
        json={
            "rating": 5,
            "comment": "Absolutely delicious"
        }
    )

    assert response.status_code == 200
    assert response.json()["rating"] == 5
    assert response.json()["comment"] == "Absolutely delicious"


def test_update_rating_partial(client):
    recipe_response = client.post(
        "/recipes",
        json={"name": "Chocolate Cake"}
    )
    recipe_id = recipe_response.json()["id"]

    client.post(
        f"/recipes/{recipe_id}/rating",
        json={
            "rating": 4,
            "comment": "Pretty good"
        }
    )

    response = client.put(
        f"/recipes/{recipe_id}/rating",
        json={"comment": "Actually, really good"}
    )

    assert response.status_code == 200
    assert response.json()["rating"] == 4
    assert response.json()["comment"] == "Actually, really good"


def test_update_rating_recipe_not_found(client):
    response = client.put(
        "/recipes/-1/rating",
        json={"rating": 5}
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Recipe not found"


def test_update_rating_not_found(client):
    recipe_response = client.post(
        "/recipes",
        json={"name": "Chocolate Cake"}
    )
    recipe_id = recipe_response.json()["id"]

    response = client.put(
        f"/recipes/{recipe_id}/rating",
        json={"rating": 5}
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Rating not found"


def test_update_rating_invalid_value(client):
    recipe_response = client.post(
        "/recipes",
        json={"name": "Chocolate Cake"}
    )
    recipe_id = recipe_response.json()["id"]

    client.post(
        f"/recipes/{recipe_id}/rating",
        json={"rating": 4}
    )

    response = client.put(
        f"/recipes/{recipe_id}/rating",
        json={"rating": 6}
    )

    assert response.status_code == 422


def test_delete_rating(client):
    recipe_response = client.post(
        "/recipes",
        json={"name": "Chocolate Cake"}
    )
    recipe_id = recipe_response.json()["id"]

    client.post(
        f"/recipes/{recipe_id}/rating",
        json={"rating": 5}
    )

    response = client.delete(f"/recipes/{recipe_id}/rating")

    assert response.status_code == 204

    rating_response = client.get(f"/recipes/{recipe_id}/rating")
    assert rating_response.status_code == 404
    assert rating_response.json()["detail"] == "Rating not found"


def test_delete_rating_recipe_not_found(client):
    response = client.delete("/recipes/-1/rating")

    assert response.status_code == 404
    assert response.json()["detail"] == "Recipe not found"


def test_delete_rating_not_found(client):
    recipe_response = client.post(
        "/recipes",
        json={"name": "Chocolate Cake"}
    )
    recipe_id = recipe_response.json()["id"]

    response = client.delete(f"/recipes/{recipe_id}/rating")

    assert response.status_code == 404
    assert response.json()["detail"] == "Rating not found"


def test_delete_recipe_cascades_rating(client, db_session):
    recipe_response = client.post(
        "/recipes",
        json={"name": "Chocolate Cake"}
    )
    recipe_id = recipe_response.json()["id"]

    client.post(
        f"/recipes/{recipe_id}/rating",
        json={"rating": 5, "comment": "Delicious"}
    )

    response = client.delete(f"/recipes/{recipe_id}")

    assert response.status_code == 204

    recipe = db_session.get(Recipe, recipe_id)
    assert recipe is None

    rating = db_session.query(Rating).filter_by(recipe_id=recipe_id).first()
    assert rating is None
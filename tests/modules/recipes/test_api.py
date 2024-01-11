from rest_framework import status

from food_r.modules.recipes.models import Recipe


def test_recipe_create(api_user_client1):
    response = api_user_client1.post(
        "/api/recipe/",
        data={
            "name": "recipe 22",
            "text": "Text test",
            "ingredients": [
                {"name": "ing 1"},
                {"name": "ing 2"},
                {"name": "ing 3"},
                {"name": "ing 4"},
            ],
        },
        format="json",
    )

    assert response.status_code == status.HTTP_201_CREATED
    recipe = Recipe.objects.first()
    response_data = response.json()
    assert response_data["id"] == recipe.id
    assert response_data["name"] == "recipe 22"
    assert response_data["text"] == "Text test"


def test_recipe_get(api_user_client1, recipe, ingredient_1, ingredient_2):
    response = api_user_client1.get(
        f"/api/recipe/{recipe.id}/",
        format="json",
    )

    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert response_data == {
        "id": recipe.id,
        "name": "Recipe 1",
        "text": "recipe text",
        "ingredients": [
            {"id": ingredient_1.id, "name": "ingredient 1"},
            {"id": ingredient_2.id, "name": "ingredient 2"},
        ],
        "average_rating": None,
    }


def test_recipe_list_get(api_user_client1, recipe, ingredient_1, ingredient_2):
    response = api_user_client1.get(
        "/api/recipe/",
        format="json",
    )

    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert response_data == {
        "count": 1,
        "next": None,
        "previous": None,
        "results": [
            {
                "id": recipe.id,
                "name": "Recipe 1",
                "text": "recipe text",
                "ingredients": [
                    {"id": ingredient_1.id, "name": "ingredient 1"},
                    {"id": ingredient_2.id, "name": "ingredient 2"},
                ],
                "average_rating": None,
            }
        ],
    }


def test_recipe_own_get(api_user_client1, recipe, ingredient_1, ingredient_2):
    response = api_user_client1.get(
        "/api/recipe/own/",
        format="json",
    )
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert response_data == {
        "count": 1,
        "next": None,
        "previous": None,
        "results": [
            {
                "id": recipe.id,
                "name": "Recipe 1",
                "text": "recipe text",
                "ingredients": [
                    {"id": ingredient_1.id, "name": "ingredient 1"},
                    {"id": ingredient_2.id, "name": "ingredient 2"},
                ],
                "average_rating": None,
            }
        ],
    }


def test_recipe_rating(api_user_client2, recipe):
    response = api_user_client2.post(
        f"/api/recipe/rating/{recipe.id}/",
        data={"rate": 3.2},
        format="json",
    )

    assert response.status_code == status.HTTP_201_CREATED
    response_data = response.json()
    assert response_data["average_rating"] == "3.2"


def test_recipe_rating_own(api_user_client1, recipe):
    response = api_user_client1.post(
        f"/api/recipe/rating/{recipe.id}/",
        data={"rate": 3.2},
        format="json",
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN
    response_data = response.json()
    assert (
        response_data["detail"] == "You do not have permission to perform this action."
    )

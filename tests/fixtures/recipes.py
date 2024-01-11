from datetime import datetime

import pytest
import pytz
from freezegun import freeze_time

from food_r.modules.recipes.models import Recipe, Ingredient, Rating


@pytest.fixture
@freeze_time("2024-01-01 22:00:00")
def ingredient_1(django_user_model):
    ingredient = Ingredient.objects.create(
        name="ingredient 1", created=datetime(2020, 8, 1, tzinfo=pytz.UTC)
    )
    return ingredient


@pytest.fixture
@freeze_time("2024-01-01 22:00:00")
def ingredient_2(django_user_model):
    ingredient = Ingredient.objects.create(
        name="ingredient 2", created=datetime(2020, 8, 1, tzinfo=pytz.UTC)
    )
    return ingredient


@pytest.fixture
@freeze_time("2024-01-01 22:00:00")
def recipe(django_user_model, user1, ingredient_1, ingredient_2):
    recipe = Recipe.objects.create(
        name="Recipe 1",
        text="recipe text",
        created_by=user1,
        created=datetime(2020, 8, 1, tzinfo=pytz.UTC),
    )
    recipe.ingredients.set([ingredient_1, ingredient_2])
    return recipe


@pytest.fixture
@freeze_time("2024-01-01 22:00:00")
def rating(django_user_model, user1, recipe):
    rating = Rating.objects.create(
        rate=2.5,
        recipe=recipe,
        user=user1,
        created=datetime(2020, 8, 1, tzinfo=pytz.UTC),
    )
    return rating

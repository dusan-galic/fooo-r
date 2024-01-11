from typing import List

from rest_framework.routers import SimpleRouter

from food_r.modules.recipes.api.views import (
    IngredientMostUsedView,
    RecipeListOwnView,
    RecipeMaxIngredients,
    RecipeMinIngredients,
    RecipeRatingView,
    RecipeSearchView,
    RecipeView,
)

router = SimpleRouter()
router.register(
    r"recipe/top_ingredient", IngredientMostUsedView, basename="top_ingredient"
)
router.register(r"recipe/search", RecipeSearchView, basename="recipe_search")
router.register(r"recipe/max", RecipeMaxIngredients, basename="recipe_max")
router.register(r"recipe/min", RecipeMinIngredients, basename="recipe_min")
router.register(r"recipe/own", RecipeListOwnView, basename="recipe_own")

router.register(r"recipe", RecipeView, basename="recipe")
router.register(
    r"recipe/rating/(?P<recipe_id>\d+)", RecipeRatingView, basename="recipe_rating"
)

urlpatterns: List = []
urlpatterns += router.urls

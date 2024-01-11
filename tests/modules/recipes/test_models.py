def test_recipe_str_method(recipe):
    assert str(recipe) == "Recipe 1"


def test_ingredient_str_method(ingredient_1):
    assert str(ingredient_1) == "ingredient 1"


def test_rating_str_method(rating):
    assert str(rating) == "Recipe 1 - 2.5"

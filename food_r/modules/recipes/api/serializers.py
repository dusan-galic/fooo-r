from django.core.exceptions import ValidationError
from rest_framework import serializers

from food_r.modules.recipes.models import Ingredient, Recipe


def validate_rate(value):
    if value < 1 or value > 5:
        raise ValidationError(
            "%(value)s is not number between 1 and 5",
            params={"value": value},
        )


class IngredientBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = (
            "id",
            "name",
        )


class IngredientTopUsedSerializer(IngredientBaseSerializer):
    num_ing = serializers.IntegerField()

    class Meta:
        model = Ingredient
        fields = IngredientBaseSerializer.Meta.fields + ("num_ing",)


class RecipeBaseSerializer(serializers.ModelSerializer):
    ingredients = IngredientBaseSerializer(many=True)
    average_rating = serializers.DecimalField(
        decimal_places=1, default=0.0, max_digits=2, read_only=True
    )

    class Meta:
        model = Recipe
        fields = (
            "id",
            "name",
            "text",
            "ingredients",
            "average_rating",
        )


class RecipeRatingSerializer(serializers.ModelSerializer):
    rate = serializers.DecimalField(
        decimal_places=1, max_digits=2, required=True, validators=[validate_rate]
    )

    class Meta:
        model = Recipe
        fields = ("rate",)

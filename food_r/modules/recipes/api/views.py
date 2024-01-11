from typing import Dict

from django.db.models import Count
from drf_yasg.utils import swagger_auto_schema
from rest_framework import filters, status
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from food_r.extensions.rest_framework.pagination import ResultsSetPagination
from food_r.modules.recipes.api.serializers import (
    IngredientTopUsedSerializer,
    RecipeBaseSerializer,
    RecipeRatingSerializer,
)
from food_r.modules.recipes.models import Ingredient, Rating, Recipe


class RecipeView(ListModelMixin, RetrieveModelMixin, CreateModelMixin, GenericViewSet):
    serializer_class = RecipeBaseSerializer
    queryset = Recipe.objects.all()

    pagination_class = ResultsSetPagination

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        ingredients_data = validated_data.pop("ingredients")
        ingredients: Dict = {
            ingredient.name: ingredient
            for ingredient in Ingredient.objects.filter(
                name__in=[ingredient["name"] for ingredient in ingredients_data]
            ).all()
        }

        # Create the ingredient if it is not in the db.
        for ingredient in ingredients_data:
            if ingredient["name"] not in ingredients.keys():
                ingredient = Ingredient.objects.create(name=ingredient["name"])
                ingredients[ingredient.name] = ingredient

        # Create recipe and add ingredients.
        recipe = Recipe.objects.create(**validated_data, created_by_id=request.user.id)
        for ingredient in ingredients.values():
            recipe.ingredients.add(ingredient)

        recipe_data = RecipeBaseSerializer(recipe).data
        return Response(recipe_data, status=status.HTTP_201_CREATED)


class RecipeListOwnView(ListModelMixin, GenericViewSet):
    serializer_class = RecipeBaseSerializer

    def list(self, request, *args, **kwargs):
        queryset = Recipe.objects.filter(created_by_id=request.user.id).all()

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class RecipeRatingView(CreateModelMixin, GenericViewSet):
    serializer_class = RecipeRatingSerializer
    queryset = Recipe.objects.all()

    @swagger_auto_schema(responses={status.HTTP_201_CREATED: RecipeBaseSerializer})
    def create(self, request, recipe_id=None, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        recipe = Recipe.objects.filter(id=recipe_id).first()
        if not recipe:
            raise NotFound("Recipe not found.")

        if request.user.id == recipe.created_by_id:
            raise PermissionDenied()

        Rating.objects.create(
            rate=validated_data["rate"], recipe_id=recipe.id, user_id=request.user.id
        )

        recipe_data = RecipeBaseSerializer(recipe).data
        return Response(recipe_data, status=status.HTTP_201_CREATED)


class IngredientMostUsedView(ListModelMixin, GenericViewSet):
    serializer_class = IngredientTopUsedSerializer
    queryset = (
        Ingredient.objects.all()
        .annotate(num_ing=Count("recipe"))
        .order_by("-num_ing")[:5]
    )

    pagination_class = None


class RecipeSearchView(ListModelMixin, GenericViewSet):
    serializer_class = RecipeBaseSerializer
    queryset = Recipe.objects.all()

    filter_backends = [filters.SearchFilter]
    search_fields = ["name", "text", "ingredients__name"]

    pagination_class = ResultsSetPagination


class RecipeMaxIngredients(ListModelMixin, GenericViewSet):
    serializer_class = RecipeBaseSerializer

    def list(self, request, *args, **kwargs):
        queryset = (
            Recipe.objects.values().order_by().annotate(num_ing=Count("ingredients"))
        )
        max_ing_num = max(_["num_ing"] for _ in queryset)
        max_recipes = [
            recipe for recipe in queryset if recipe["num_ing"] == max_ing_num
        ]

        return Response(max_recipes)


class RecipeMinIngredients(ListModelMixin, GenericViewSet):
    serializer_class = RecipeBaseSerializer

    def list(self, request, *args, **kwargs):
        queryset = (
            Recipe.objects.values().order_by().annotate(num_ing=Count("ingredients"))
        )
        min_ing_num = min(_["num_ing"] for _ in queryset)
        min_recipes = [
            recipe for recipe in queryset if recipe["num_ing"] == min_ing_num
        ]

        return Response(min_recipes)

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Avg

from food_r.extensions.database.mixins import TimestampMixin


def validate_rate(value):
    if value < 1 or value > 5:
        raise ValidationError(
            "%(value)s is not number between 1 and 5",
            params={"value": value},
        )


class Ingredient(TimestampMixin, models.Model):
    name = models.CharField(max_length=50, null=False)

    def __str__(self) -> str:
        return f"{self.name}"


class Recipe(TimestampMixin, models.Model):
    name = models.CharField(max_length=50, null=False)
    text = models.TextField(null=False)
    ingredients = models.ManyToManyField(Ingredient)

    created_by = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="recipe_created",
    )

    def __str__(self) -> str:
        return f"{self.name}"

    @property
    def average_rating(self):
        return self.rating_set.all().aggregate(Avg("rate"))["rate__avg"]


class Rating(TimestampMixin, models.Model):
    rate = models.DecimalField(max_digits=2, decimal_places=1)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="rating_user",
    )

    def __str__(self) -> str:
        return f"{self.recipe} - {self.rate}"

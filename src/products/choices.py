from django.db import models


class ProductCategoryChoice(models.TextChoices):
    VEGETABLE = "VEGETABLE"
    FRUIT = "FRUIT"
    DRY_FRUIT = "DRY_FRUIT"
    BREAD = "BREAD"
    MEAT = "MEAT"

class RatingChoices(models.IntegerChoices):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5


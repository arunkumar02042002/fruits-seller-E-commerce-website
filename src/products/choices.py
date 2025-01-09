from django.db import models


class ProductCategoryChoice(models.TextChoices):
    VEGETABLE = "VEGETABLE"
    FRUIT = "FRUIT"
    DRY_FRUIT = "DRY_FRUIT"
    BREAD = "BREAD"
    MEAT = "MEAT"

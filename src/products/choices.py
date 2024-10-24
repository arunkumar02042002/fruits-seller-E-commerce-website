from django.db import models


class ProductCategoryChoice(models.TextChoices):
    VEGETABLE = "VEGITABLE"
    FRUIT = "FRUIT"
    DRY_FRUIT = "DRY_FRUITS"
    BREAD = "BREAD"
    MEAT = "MEAT"

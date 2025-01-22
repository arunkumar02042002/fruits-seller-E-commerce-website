from django.core.management.base import BaseCommand
from products.models import Tag


class Command(BaseCommand):
    help = "Add 20 tags to the database"

    def handle(self, *args, **kwargs):
        tag_titles = [
            "fruit",
            "vegetable",
            "organic",
            "fresh",
            "exotic",
            "seasonal",
            "local",
            "imported",
            "dried",
            "tropical",
            "berries",
            "citrus",
            "melons",
            "stonefruit",
            "leafy",
            "root",
            "gourds",
            "nuts",
            "seeds",
            "spices",
            "bread",
            "wholegrain",
            "sourdough",
            "baguette",
            "rye",
            "meat",
            "poultry",
            "beef",
            "pork",
            "lamb",
            "seafood",
            "fish",
            "shellfish",
            "dry fruits",
            "raisins",
            "dates",
            "figs",
            "apricots",
            "prunes",
            "herbs",
            "microgreens",
            "sprouts",
            "fermented",
            "pickled",
            "canned",
            "frozen",
            "juices",
            "smoothies",
            "salads",
            "soups",
            "stews",
            "grains",
            "legumes",
            "pasta",
            "rice",
            "quinoa",
            "barley",
            "oats",
            "millet"
        ]

        for title in tag_titles:
            tag, created = Tag.objects.get_or_create(title=title)
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f"Successfully created tag: {tag.title}")
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f"Tag already exists: {tag.title}")
                )

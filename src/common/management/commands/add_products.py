import random
import uuid

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from faker import Faker

from authentication.choices import UserRoleChoices

from products.models import Product, Tag
from products.choices import ProductCategoryChoice



User = get_user_model()


class Command(BaseCommand):
    help = "Add 50 products and associate them with random tags"

    def handle(self, *args, **kwargs):
        fake = Faker()

        # Check if at least 10 tags exist, if not, create some default ones
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
        ]

        # Add tags if they don't exist
        tags = []
        for title in tag_titles:
            tag, created = Tag.objects.get_or_create(title=title)
            tags.append(tag)

        # Create a dummy user to associate with products (or use an existing user)
        admin_user, _ = User.objects.get_or_create(
            username="admin_user",
            is_staff=True,
            role=UserRoleChoices.ADMIN
        )

        # Generate 50 products
        for _ in range(50):
            product = Product.objects.create(
                uuid=uuid.uuid4(),
                name=fake.word().capitalize(),
                description=fake.paragraph(nb_sentences=3),
                category=random.choice(ProductCategoryChoice.choices),
                sub_category=random.choice(
                    ["Berries", "Melons", "leafy", "melons", "gourds"]
                ),
                discount_in_percent=random.uniform(0, 50),
                price=round(random.uniform(10.00, 500.00), 2),
                created_by=admin_user,
            )

            # Randomly assign tags (between 1 and 5 tags per product)
            assigned_tags = random.sample(tags, k=random.randint(1, 5))
            product.tags.set(assigned_tags)

            # Output success message
            self.stdout.write(
                self.style.SUCCESS(
                    f"Successfully created product: {product.name} with {len(assigned_tags)} tags."
                )
            )

        self.stdout.write(self.style.SUCCESS("Successfully added 50 products!"))

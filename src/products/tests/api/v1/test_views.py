import time

from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from products.choices import ProductCategoryChoice
from products.factories import ProductFactory, TagFactory


class ProductListViewTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.url = reverse("products")
        return super().setUp()

    def test_product_list_view(self):
        """Test product listing."""
        ProductFactory(name="Fresh Apples", price=50)
        time.sleep(0.1)
        ProductFactory(name="Organic Bananas", price=100)

        response = self.client.get(self.url)
        data = response.data
        
        self.assertEqual(data["status"], "success")
        self.assertEqual(data["message"], "Products fetched successfully.")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data["payload"]["results"]), 2)
        self.assertEqual(data["payload"]["results"][0]["name"], "Organic Bananas")
    
    def test_product_list_view_pagination(self):
        """Test pagination."""
        ProductFactory.create_batch(12)

        url = reverse("products")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["payload"]["results"]), 9)
        self.assertEqual(response.data["payload"]["current"], 1)
        self.assertEqual(response.data["payload"]["start"], 1)
        self.assertEqual(response.data["payload"]["next"], 2)
        self.assertEqual(response.data["payload"]["previous"], None)
        self.assertEqual(response.data["payload"]["last"], 2)
        self.assertEqual(response.data["payload"]["count"], 12)


    def test_product_list_view_ordering(self):
        """Test product ordering"""
        p1 = ProductFactory(
            name="Expensive Product", price=500,
            discount_in_percent = 15.00
        )
        time.sleep(0.1)
        p2 = ProductFactory(
            name="Cheap Product", price=10,
            discount_in_percent=12.00
        )

        response = self.client.get(self.url, {"ordering": "price"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["payload"]["results"][0]["name"], "Cheap Product")

        response = self.client.get(self.url, {"ordering": "-price"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["payload"]["results"][0]["name"], "Expensive Product")

        response = self.client.get(self.url, {"ordering": "-created_at"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["payload"]["results"][0]["name"], "Cheap Product")

        response = self.client.get(self.url, {"ordering": "created_at"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["payload"]["results"][0]["name"], "Expensive Product")

        response = self.client.get(self.url, {"ordering": "discount_in_percent"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["payload"]["results"][0]["name"], "Cheap Product")

        response = self.client.get(self.url, {"ordering": "-discount_in_percent"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["payload"]["results"][0]["name"], "Expensive Product")

        p2.discount_in_percent = 13.00
        p2.save()

        response = self.client.get(self.url, {"ordering": "updated_at"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["payload"]["results"][0]["name"], "Expensive Product")

        response = self.client.get(self.url, {"ordering": "-updated_at"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["payload"]["results"][0]["name"], "Cheap Product")

    def test_product_search(self):
        ProductFactory(
            name="Fresh Apples", category=ProductCategoryChoice.FRUIT,
            sub_category='Citrus',
            description="Fresh Apples are healthy and sweet."
        )
        ProductFactory(
            name="Fresh Carrots", category=ProductCategoryChoice.VEGETABLE,
            sub_category='Root Vegetable',
            description="Fresh Carrots are healthy."
        )
        ProductFactory(
            name="Fresh Brinjal", category=ProductCategoryChoice.VEGETABLE,
            sub_category='Fruit Vegetable',
            description="Fresh Brinjal is a healthy vegetable."
        )

        # Sub Category Search
        response = self.client.get(self.url, {'search':'root'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["payload"]["results"]), 1)

        response = self.client.get(self.url, {'search':'vegetable'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["payload"]["results"]), 2)

        # Name Search
        response = self.client.get(self.url, {'search':'fresh'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["payload"]["results"]), 3)

        response = self.client.get(self.url, {'search':'brinj'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["payload"]["results"]), 1)

        # Description Search
        response = self.client.get(self.url, {'search':'sweet'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["payload"]["results"]), 1)

    def test_product_category_filtering(self):
        """Test category wise filtering."""
        ProductFactory(
            name="Fresh Apples", category=ProductCategoryChoice.FRUIT
        )
        ProductFactory(
            name="Fresh Carrots", category=ProductCategoryChoice.VEGETABLE
        )

        response = self.client.get(self.url, {"category": "FRUIT"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["payload"]["results"]), 1)
        self.assertEqual(response.data["payload"]["results"][0]["name"], "Fresh Apples")

    def test_product_name_filter(self):
        """Test filter by product name."""
        ProductFactory(
            name="Fresh Apples", category=ProductCategoryChoice.FRUIT
        )
        ProductFactory(
            name="Fresh Carrots", category=ProductCategoryChoice.VEGETABLE
        )

        response = self.client.get(self.url, {"name": "apple"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["payload"]["results"]), 1)
        self.assertEqual(response.data["payload"]["results"][0]["name"], "Fresh Apples")

    def test_product_sub_category_filter(self):
        """Test filter by product name."""
        ProductFactory(
            name="Fresh Oranges", category=ProductCategoryChoice.FRUIT,
            sub_category='Citrus'
        )
        ProductFactory(
            name="Fresh Carrots", category=ProductCategoryChoice.VEGETABLE,
            sub_category='Root Vegetable'
        )

        response = self.client.get(self.url, {"sub_category": "root"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["payload"]["results"]), 1)
        self.assertEqual(response.data["payload"]["results"][0]["name"], "Fresh Carrots")

    def test_product_tag_title_filter(self):
        tags = [
            TagFactory(title='healthy'), TagFactory(title='sweet')
        ]
        ProductFactory(
            name="Fresh Apples", category=ProductCategoryChoice.FRUIT,
            tags = [tags[0], tags[1]]
        )
        ProductFactory(
            name="Fresh Carrots", category=ProductCategoryChoice.VEGETABLE,
            tags = [tags[0]]
        )
        ProductFactory(
            name="Fresh Brinjal", category=ProductCategoryChoice.VEGETABLE
        )

        response = self.client.get(self.url, {"tags": ["healthy", "sweet"]})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["payload"]["results"]), 1)
        self.assertEqual(response.data["payload"]["results"][0]["name"], "Fresh Apples")

        response = self.client.get(self.url, {"tags": "healthy"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["payload"]["results"]), 2)

        response = self.client.get(self.url, {"tags": ["sweet"]})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["payload"]["results"]), 1)
        self.assertEqual(response.data["payload"]["results"][0]["name"], "Fresh Apples")

    def test_product_price_filter(self):
        ProductFactory(name="Fresh Apples", price=50)
        ProductFactory(name="Organic Bananas", price=100)

        response = self.client.get(self.url, {'min_price':50})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["payload"]["results"]), 2)

        response = self.client.get(self.url, {'min_price':100})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["payload"]["results"]), 1)
        self.assertEqual(response.data["payload"]["results"][0]["name"], "Organic Bananas")

        response = self.client.get(self.url, {'min_price':101})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["payload"]["results"]), 0)

        response = self.client.get(self.url, {'max_price':100})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["payload"]["results"]), 2)

        response = self.client.get(self.url, {'max_price':50})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["payload"]["results"]), 1)
        self.assertEqual(response.data["payload"]["results"][0]["name"], "Fresh Apples")

        response = self.client.get(self.url, {'max_price':49})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["payload"]["results"]), 0)

    def test_product_discount_filter(self):
        ProductFactory(
            name="Fresh Apples", price=50, discount_in_percent=10
        )
        ProductFactory(
            name="Organic Bananas", price=100, discount_in_percent=15
        )

        response = self.client.get(self.url, {'min_discount':10})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["payload"]["results"]), 2)

        response = self.client.get(self.url, {'min_discount':15})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["payload"]["results"]), 1)
        self.assertEqual(response.data["payload"]["results"][0]["name"], "Organic Bananas")

        response = self.client.get(self.url, {'min_discount':16})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["payload"]["results"]), 0)

        response = self.client.get(self.url, {'max_discount':15})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["payload"]["results"]), 2)

        response = self.client.get(self.url, {'max_discount':10})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["payload"]["results"]), 1)
        self.assertEqual(response.data["payload"]["results"][0]["name"], "Fresh Apples")

        response = self.client.get(self.url, {'max_discount':9})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["payload"]["results"]), 0)


class TagListView(TestCase):
    """Test Tag List View."""

    def setUp(self):
        self.client = APIClient()
        self.url = reverse("tags")
    
    def test_tag_list_view(self):
        """Test tag listing."""
        TagFactory(title="healthy")
        TagFactory(title="sweet")

        response = self.client.get(self.url)
        data = response.data

        self.assertEqual(data["status"], "success")
        self.assertEqual(data["message"], "Tags fetched successfully.")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data["payload"]["tags"]), 2)

    def test_tag_list_view_ordering(self):
        """Test tag ordering."""
        t1 = TagFactory(title="healthy")
        time.sleep(0.2)
        t2 = TagFactory(title="sweet")

        response = self.client.get(self.url, {"ordering": "title"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["payload"]["tags"][0]["title"], t1.title)

        response = self.client.get(self.url, {"ordering": "-title"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["payload"]["tags"][0]["title"], t2.title)

        response = self.client.get(self.url, {"ordering": "-created_at"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["payload"]["tags"][0]["title"], t2.title)

        response = self.client.get(self.url, {"ordering": "created_at"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["payload"]["tags"][0]["title"], t1.title)

    def test_tag_search(self):
        TagFactory(title="healthy")
        TagFactory(title="sweet")

        response = self.client.get(self.url, {'title':'heal'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["payload"]["tags"]), 1)

        response = self.client.get(self.url, {'title':'sweet'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["payload"]["tags"]), 1)

        response = self.client.get(self.url, {'title':'swe'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["payload"]["tags"]), 1)

        response = self.client.get(self.url, {'title':'sour'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["payload"]["tags"]), 0)

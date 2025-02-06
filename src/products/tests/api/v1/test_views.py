from datetime import timedelta
from decimal import Decimal
import time

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from rest_framework import status
from rest_framework.test import APIClient

from products.choices import ProductCategoryChoice
from products.factories import (
    CouponFactory,
    ProductFactory, TagFactory
)

from users.factories import (
    CartFactory,
    CartItemFactory,
    UserProfileFactory
)


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


class CheckCouponViewTest(TestCase):
    """Test Check Coupon View."""

    def setUp(self):
        self.client = APIClient()
        self.profile = UserProfileFactory()
        self.cart = CartFactory(profile=self.profile)
        self.p1 = ProductFactory(price=50, discount_in_percent=10)
        self.p2 = ProductFactory(price=100, discount_in_percent=20)
        self.cart_item = CartItemFactory(cart=self.cart, product=self.p1, quantity=2)
        self.cart_item = CartItemFactory(cart=self.cart, product=self.p2, quantity=1)
        self.coupon1 = CouponFactory(
            code="code1",
            discount=10,
            min_price_required=50,
            is_always_valid=True,
            valid_from=None,
            valid_to=None
        )
        self.coupon2 = CouponFactory(
            code="code2",
            discount=10,
            min_price_required=100,
        )
        self.inactiveCoupon = CouponFactory(
            code="code3",
            discount=10,
            min_price_required=100,
            active=False
        )
        self.expiredCoupon = CouponFactory(
            code="code4",
            discount=10,
            min_price_required=100,
            valid_from=timezone.now() - timedelta(days=30),
            valid_to=timezone.now() - timedelta(days=1)
        )
        self.minPriceHighCoupon = CouponFactory(
            code="code5",
            discount=10,
            min_price_required=Decimal('10000.00'),
            is_always_valid=True,
        )
        self.sub_total = (
            self.p1.discounted_price * 2 + self.p2.discounted_price
        )
        self.delivery_fee = Decimal("99.00")
        self.url = reverse("check-coupon")
    

    def test_check_inactive_coupon(self):
        """Test inactive coupon check."""
        response = self.client.post(self.url, {"code": "code3"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["status"], "error")
        self.assertEqual(response.data["message"], "code: Could not find coupon.")

    def test_check_invalid_coupon_code(self):
        """Test invalid coupon check."""
        response = self.client.post(self.url, {"code": "code-1"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["status"], "error")
        self.assertEqual(response.data["message"], "code: Invalid coupon code.")
        self.assertEqual(response.data["payload"]["errors"]["code"][0], "Invalid coupon code.")

    def test_check_expired_coupon(self):
        """Test expired coupon check."""
        response = self.client.post(self.url, {"code": "code4"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["status"], "error")
        self.assertEqual(response.data["message"], "code: Could not find coupon.")
        self.assertEqual(response.data["payload"]["errors"]["code"][0], "Could not find coupon.")

    def test_min_price_required_is_greater(self):
        """Test min price required is greater."""
        response = self.client.post(self.url, {"code": "code5"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["status"], "error")
        self.assertEqual(response.data["message"], "Coupon code is not valid.")
        self.assertEqual(
            response.data["payload"]["error"]["code"][0],
            f"Minimum order price required {self.minPriceHighCoupon.min_price_required}."
        )

    def test_check_always_valid_coupon(self):
        """Test always valid coupon check."""
        self.client.force_authenticate(user=self.profile.user)
        response = self.client.post(self.url, {"code": "code1"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "success")
        self.assertEqual(response.data["message"], "Coupon code applied successfully.")
        self.assertEqual(response.data["payload"]["discount"], 10)
        self.assertEqual(response.data["payload"]["code"], self.coupon1.code)
        self.assertEqual(response.data["payload"]["sub_total"], self.sub_total)
        self.assertEqual(response.data["payload"]["delivery_fee"], self.delivery_fee)
        self.assertEqual(response.data["payload"]["total"], self.sub_total + self.delivery_fee)
        self.assertEqual(response.data["payload"]["discounted_total"], self.sub_total + self.delivery_fee - self.coupon1.discount)

    def test_check_a_valid_coupon(self):
        """Test a valid coupon check."""
        self.client.force_authenticate(user=self.profile.user)
        response = self.client.post(self.url, {"code": "code2"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "success")
        self.assertEqual(response.data["message"], "Coupon code applied successfully.")
        self.assertEqual(response.data["payload"]["discount"], 10)
        self.assertEqual(response.data["payload"]["code"], self.coupon2.code)
        self.assertEqual(response.data["payload"]["sub_total"], self.sub_total)
        self.assertEqual(response.data["payload"]["delivery_fee"], self.delivery_fee)
        self.assertEqual(response.data["payload"]["total"], self.sub_total + self.delivery_fee)
        self.assertEqual(response.data["payload"]["discounted_total"], self.sub_total + self.delivery_fee - self.coupon2.discount)


class AddReviewAPIViewTest(TestCase):
    """Test Add Review API View."""
    def setUp(self):
        """Set up data."""
        self.client = APIClient()

    def test_add_review_unauthenticated(self):
        """Test add review unauthenticated."""
        p = ProductFactory()
        url = reverse("add-review", kwargs={"uuid": p.uuid})
        response = self.client.post(
            url,
            {"rating": 4, "review": "Good Product"}
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data["status"], "error")
    
    def test_add_review_authenticated(self):
        """Test add review authenticated."""
        profile = UserProfileFactory()
        p = ProductFactory()
        url = reverse("add-review", kwargs={"uuid": p.uuid})
        self.client.force_authenticate(user=profile.user)
        response = self.client.post(url, {"rating": 4, "review": "Good Product"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["status"], "success")
        self.assertEqual(response.data["message"], "Product review added successfully.")
        self.assertEqual(response.data["payload"]["rating"], 4)
        self.assertEqual(response.data["payload"]["review"], "Good Product")
        self.assertEqual(response.data["payload"]["profile"], profile.uuid)
        self.assertEqual(response.data["payload"]["product"], p.uuid)

    def test_wrong_review_data(self):
        """Test wrong review data."""
        profile = UserProfileFactory()
        p = ProductFactory()
        url = reverse("add-review", kwargs={"uuid": p.uuid})
        self.client.force_authenticate(user=profile.user)
        response = self.client.post(url, {"rating": 6, "review": "Good Product"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["status"], "error")
        self.assertEqual(response.data["message"], 'rating: "6" is not a valid choice.')

        response = self.client.post(url, {"rating": 4, "review": ""})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["status"], "error")
        self.assertEqual(response.data["message"], 'review: This field may not be blank.')

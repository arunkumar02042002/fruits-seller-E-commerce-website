import io
import time

from PIL import Image
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile

from main.models import Testimonial

User = get_user_model()


class TestimonialAddViewTests(APITestCase):

    TESTING_THRESHOLD = "2/min"

    def setUp(self):
        # Create a user and obtain authentication token
        self.user = User.objects.create_user(
            username="testuser", email="testuser@example.com", password="testpassword"
        )
        self.user2 = User.objects.create_user(
            username="testuser2", email="testuser2@example.com", password="testpassword"
        )
        self.client = APIClient()

        # Define the URL for the TestimonialAddView
        self.url = reverse("testimonial-add")  # Adjust this to match your URL name

        # Valid testimonial data
        self.valid_data = {
            "name": "John Doe",
            "profession": "Engineer",
            "email": "johndoe@example.com",
            "feedback": "Great service!",
            "rating": "5",
        }

    # def generate_image(self):
    #     """Helper function to generate a valid image file in memory."""
    #     image = Image.new("RGB", (100, 100), color="red")
    #     image_io = io.BytesIO()
    #     image.save(image_io, format="JPEG")
    #     image_io.seek(0)
    #     return SimpleUploadedFile(
    #         name="test_image.jpg", content=image_io.read(), content_type="image/jpeg"
    #     )

    def test_authentication_required(self):
        """Test that authentication is required to access the view."""
        response = self.client.post(self.url, data=self.valid_data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_testimonial(self):
        """Test successful creation of a testimonial."""

        self.client.force_login(user=self.user)
        response = self.client.post(self.url, data=self.valid_data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Testimonial.objects.count(), 1)

        testimonial = Testimonial.objects.first()
        self.assertEqual(testimonial.name, self.valid_data["name"])
        self.assertEqual(testimonial.email, self.valid_data["email"])
        self.assertEqual(testimonial.profession, self.valid_data["profession"])
        self.assertEqual(testimonial.feedback, self.valid_data["feedback"])
        self.assertEqual(testimonial.rating, self.valid_data["rating"])

    def test_create_testimonial_invalid_data(self):
        """Test that invalid data returns a 400 response."""
        invalid_data = self.valid_data.copy()
        invalid_data["name"] = ""
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, data=invalid_data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_restrict_min_throttling(self):
        """Test that throttling is enforced after exceeding request limit."""

        self.client.force_login(user=self.user2)

        for _ in range(2):
            response = self.client.post(
                self.url, data=self.valid_data, format="multipart"
            )
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Third request should hit the throttle limit
        response = self.client.post(self.url, data=self.valid_data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)

    # def test_restrict_day_throttling(self):
    #     """
    #     Test that requests to the TestimonialAddView are throttled after exceeding the limit.

    #     Commenting this test as it requires 5 mins to complete
    #     """
    #     self.client.force_login(user=self.user)

    #     for _ in range(10):
    #         response = self.client.post(self.url, data=self.valid_data, format='multipart')
    #         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #         time.sleep(31)

    #     # Eleventh request should hit the throttle limit
    #     response = self.client.post(self.url, data=self.valid_data, format='multipart')
    #     self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)

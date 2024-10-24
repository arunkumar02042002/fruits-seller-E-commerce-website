from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class EmailValidatorApiViewTests(APITestCase):

    def setUp(self):
        # Create an active user to test duplicate email case
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="password",
            is_active=True,
        )
        self.url = reverse("validate-email")

    def test_valid_email(self):
        """Test that a valid email returns a success response."""
        data = {"email": "validemail@example.com"}

        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "success")
        self.assertEqual(response.data["message"], "Email is valid.")

    def test_duplicate_email(self):
        """Test that submitting an email of an existing active user returns an error."""
        data = {"email": "test@example.com"}

        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = response.json()
        self.assertEqual(data["status"], "error")
        self.assertEqual(
            data["message"], "email: An user with that email already exists."
        )
        self.assertEqual(
            data["payload"]["errors"]["email"][0],
            "An user with that email already exists.",
        )

    def test_invalid_email_format(self):
        """Test that an invalid email format returns a validation error."""
        data = {"email": "invalid-email"}

        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = response.json()
        self.assertEqual(response.data["status"], "error")
        self.assertEqual(
            response.data["message"], "email: Enter a valid email address."
        )
        self.assertEqual(
            response.data["payload"]["errors"]["email"][0],
            "Enter a valid email address.",
        )

    def test_missing_email(self):
        """Test that submitting without an email returns a validation error."""
        data = {}

        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = response.json()
        self.assertEqual(response.data["status"], "error")
        self.assertEqual(response.data["message"], "email: This field is required.")
        self.assertEqual(
            response.data["payload"]["errors"]["email"][0], "This field is required."
        )


class PasswordValidatorApiViewTests(APITestCase):

    def setUp(self) -> None:
        self.url = reverse("validate-password")

    def test_valid_password(self):
        """Test that a valid password returns a success response."""
        data = {"password": "StrongPass123!"}

        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()

        self.assertEqual(data["status"], "success")
        self.assertEqual(data["message"], "Password is valid.")
        self.assertEqual(len(data["payload"]), 0)

    def test_invalid_password(self):
        """Test that an invalid password returns a validation error."""
        data = {"password": "weak"}

        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = response.json()
        self.assertEqual(data["status"], "error")
        self.assertEqual(
            data["message"],
            "password: This password is too short. It must contain at least 8 characters.",
        )
        self.assertEqual(
            data["payload"]["errors"]["password"][0],
            "This password is too short. It must contain at least 8 characters.",
        )

    def test_missing_password(self):
        """Test that submitting without a password returns a validation error."""
        data = {}

        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = response.json()
        self.assertEqual(data["status"], "error")
        self.assertEqual(data["message"], "password: This field is required.")
        self.assertEqual(
            data["payload"]["errors"]["password"][0], "This field is required."
        )

    def test_common_password(self):
        """Test that a common password returns a validation error."""
        data = {"password": "password"}

        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = response.json()
        self.assertEqual(data["status"], "error")
        self.assertEqual(data["message"], "password: This password is too common.")
        self.assertEqual(
            data["payload"]["errors"]["password"][0], "This password is too common."
        )

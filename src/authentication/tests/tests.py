from unittest.mock import patch
import uuid

from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator

from authentication.tokens import account_activation_token

from users.models import Profile


User = get_user_model()


class UserModelTest(TestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_user(
            email="test@gmail.com",
            username="test_user",
            first_name="Test",
            last_name="User",
            password="testpassword",
        )
        self.superuser = User.objects.create_superuser(
            email="admin@gmail.com",
            username="admin123",
            first_name="Admin",
            last_name="User",
            password="testpassword",
        )
        self.test_uuid = 'acde070d-8c4c-4f0d-9d8a-162843c10333'

    def test_create_user(self):
        self.assertEqual(self.user.email, "test@gmail.com")
        self.assertEqual(self.user.username, "test_user")
        self.assertEqual(self.user.first_name, "Test")
        self.assertEqual(self.user.last_name, "User")
        self.assertTrue(self.user.check_password("testpassword"))
        self.assertEqual(self.user.role, "USER")
        self.assertFalse(self.user.is_staff)
        self.assertTrue(self.user.is_active)
        self.assertFalse(self.user.is_superuser)

    def test_create_superuser(self):
        self.assertEqual(self.superuser.email, "admin@gmail.com")
        self.assertEqual(self.superuser.username, "admin123")
        self.assertEqual(self.superuser.first_name, "Admin")
        self.assertEqual(self.superuser.last_name, "User")
        self.assertTrue(self.superuser.check_password("testpassword"))
        self.assertEqual(self.superuser.role, "ADMIN")
        self.assertTrue(self.superuser.is_staff)
        self.assertTrue(self.superuser.is_active)
        self.assertTrue(self.superuser.is_superuser)
        
    def test_default_values(self):
        """Test default values are being populated correctly."""
        self.assertIsNotNone(self.user.created_at)
        self.assertIsNotNone(self.user.updated_at)
        self.assertIsNone(self.user.deleted_at)
        self.assertIsNone(self.user.created_by)
        self.assertIsNone(self.user.updated_by)
        self.assertIsNone(self.user.deleted_by)

    def test_get_queryset(self):
        """Test get_queryset only returns non-deleted users."""
        self.user.delete()
        active_users = User.objects.all()
        self.assertNotIn(self.user, active_users)
        self.assertIn(self.superuser, active_users)

class SignUpViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.signup_url = reverse("signup")

    def test_get_signup_authenticated_user_redirects_to_home(self):
        """Test that an authenticated user is redirected to home"""
        user = User.objects.create_user(
            username="testuser", password="password", email="test@gmail.com"
        )
        self.client.force_login(user=user)
        response = self.client.get(self.signup_url)
        self.assertRedirects(response, reverse("home"))

    def test_get_signup_unauthenticated_user_renders_signup_form(self):
        """Test that an unauthenticated user gets the sign-up form"""
        response = self.client.get(self.signup_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "authentication/signup.html")
        self.assertIn("form", response.context)

    def test_post_signup_invalid_form(self):
        """Test that invalid form submission returns the form with errors"""
        response = self.client.post(self.signup_url, data={})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "authentication/signup.html")
        self.assertIn("form", response.context)
        self.assertTrue(response.context["form"].errors)

    @patch("authentication.views.send_mail")
    def test_post_signup_valid_form_sends_email(self, mock_send_mail):
        """Test that a valid form submission creates a user and sends email"""
        form_data = {
            "email": "test@example.com",
            "mobile_number": "1234567890",
            "password1": "testpassword123",
            "password2": "testpassword123",
            "first_name": "test",
            "last_name": "user",
        }
        response = self.client.post(self.signup_url, data=form_data)
        # Ensure the user is created
        user = User.objects.filter(email="test@example.com").first()
        self.assertIsNotNone(user)
        self.assertEqual(user.email, "test@example.com")
        self.assertEqual(user.mobile_number, "1234567890")
        self.assertEqual(user.first_name, "test")
        self.assertEqual(user.last_name, "user")
        self.assertTrue(user.check_password("testpassword123"))
        self.assertFalse(user.is_active)

        # Check that an email was sent
        mock_send_mail.assert_called_once()

        # Check the success message and redirect
        self.assertRedirects(response, self.signup_url)
        messages = list(response.wsgi_request._messages)
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]),
            "We have sent a verification link to your email. Please verify your account!",
        )

    @patch("authentication.views.send_mail", side_effect=Exception("Email error"))
    def test_post_signup_email_send_failure(self, mock_send_mail):
        """
        Test that email send failure shows error message and doesn't redirect.
        The use of @patch allows mocking the send_mail function to either simulate a successful email or an email failure.
        """
        form_data = {
            "password1": "testpassword123",
            "password2": "testpassword123",
            "email": "test@example.com",
            "mobile_number": "1234567890",
            "first_name": "test",
            "last_name": "user",
        }
        response = self.client.post(self.signup_url, data=form_data)

        # Ensure the user is created
        user = User.objects.filter(email="test@example.com").first()
        self.assertIsNotNone(user)

        # Check that the email attempt failed
        self.assertTrue(mock_send_mail.called)

        # Ensure the form is returned with an error
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "authentication/signup.html")
        self.assertTrue(response.context["form"].errors)

        # Check the error message
        messages = list(response.wsgi_request._messages)
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Error occurred while sending mail")

    @patch("django.core.mail.send_mail")
    def test_post_signup_same_email_error(self, mock_send_mail):
        """Test that submitting the same email raises an error"""
        # Create a user with the email 'test@example.com' to simulate an existing user
        User.objects.create_user(
            username="existinguser",
            email="test@example.com",
            password="existingpassword123",
        )

        # Attempt to sign up with the same email
        form_data = {
            "email": "test@example.com",
            "password1": "newpassword123",
            "password2": "newpassword123",
        }

        response = self.client.post(self.signup_url, data=form_data)

        # Check form errors
        form = response.context["form"]
        # Ensure that the form is invalid and contains the specific email error
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)
        self.assertEqual(
            form.errors["email"], ["A user with that email already exists."]
        )

        # Ensure no email is sent since the form submission failed
        mock_send_mail.assert_not_called()

        # Ensure no new user is created with the same email
        user_count = User.objects.filter(email="test@example.com").count()
        self.assertEqual(user_count, 1)  # Only the existing user should be present


class AccountActivateViewTests(TestCase):

    def setUp(self):
        # Create a test user but set it to inactive
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpassword123",
            is_active=False,  # Initially inactive
        )
        self.uidb64 = urlsafe_base64_encode(force_bytes(self.user.pk))
        self.token = account_activation_token.make_token(self.user)
        self.activate_url = reverse(
            "activate-account", kwargs={"uidb64": self.uidb64, "token": self.token}
        )

    def test_successful_activation(self):
        """Test that a user is successfully activated with valid token and uidb64"""
        response = self.client.get(self.activate_url)

        # Check that the user is activated
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_active)

        # Check user's profile is created
        self.assertTrue(Profile.objects.filter(user=self.user).exists())

        # Check that the user is redirected to the login page
        self.assertRedirects(response, reverse("login"))

    def test_invalid_uidb64(self):
        """Test that the view redirects to signup when an invalid uidb64 is used"""
        invalid_uidb64 = urlsafe_base64_encode(force_bytes(uuid.uuid4()))  # Invalid UID
        response = self.client.get(
            reverse(
                "activate-account",
                kwargs={"uidb64": invalid_uidb64, "token": self.token},
            )
        )

        # Check that the user is redirected to the signup page
        self.assertRedirects(response, reverse("signup"))

    def test_invalid_token(self):
        """Test that the view redirects to signup when an invalid token is used"""
        invalid_token = "invalid-token"
        response = self.client.get(
            reverse(
                "activate-account",
                kwargs={"uidb64": self.uidb64, "token": invalid_token},
            )
        )

        # Check that the user is redirected to the signup page
        self.assertRedirects(response, reverse("signup"))

    def test_expired_token(self):
        """Test that the view redirects to signup when an expired token is used"""
        # Mock the token to simulate expiration
        with patch(
            "authentication.tokens.account_activation_token.check_token",
            return_value=False,
        ):
            response = self.client.get(self.activate_url)

            # Check that the user is redirected to the signup page
            self.assertRedirects(response, reverse("signup"))

    def test_activation_for_non_existent_user(self):
        """Test that the view handles non-existent users correctly"""
        # Use a non-existent uid
        non_existent_uidb64 = urlsafe_base64_encode(force_bytes(uuid.uuid4()))
        response = self.client.get(
            reverse(
                "activate-account",
                kwargs={"uidb64": non_existent_uidb64, "token": self.token},
            )
        )

        # Check that the user is redirected to the signup page
        self.assertRedirects(response, reverse("signup"))


class LoginUserViewTests(TestCase):

    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpassword123"
        )
        self.login_url = reverse("login")
        self.home_url = reverse("home")

    def test_login_successful(self):
        """Test that a user can log in with valid credentials"""
        response = self.client.post(
            self.login_url,
            {"username": "test@example.com", "password": "testpassword123"},
        )
        # After successful login, the user should be redirected
        self.assertRedirects(response, self.home_url)
        # Check if the user is authenticated
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_login_invalid_credentials(self):
        """Test that login fails with invalid credentials"""
        response = self.client.post(
            self.login_url, {"email": "wrong@email.com", "password": "wrongpassword"}
        )
        # The user should not be authenticated
        self.assertFalse(response.wsgi_request.user.is_authenticated)
        # The login page should be shown again
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "authentication/login.html")

    def test_already_authenticated_user_redirect(self):
        """Test that an authenticated user trying to access the login page is redirected to home"""
        # Log the user in
        self.client.force_login(self.user)

        # Try to access the login page while authenticated
        response = self.client.get(self.login_url)

        # The user should be redirected to the home page
        self.assertRedirects(response, self.home_url)


class LogoutUserViewTests(TestCase):

    def setUp(self):
        # Create a test user and log them in
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpassword123"
        )
        self.login_url = reverse("login")
        self.logout_url = reverse("logout")
        self.client.force_login(self.user)

    def test_logout_successful(self):
        """Test that an authenticated user can log out successfully"""
        response = self.client.post(self.logout_url)

        # After logout, the user should be redirected (typically to login or home)
        self.assertRedirects(response, self.login_url)

        # The user should no longer be authenticated
        self.assertFalse(response.wsgi_request.user.is_authenticated)


class PasswordChangeViewsTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", email="test@example.com", password="testpassword"
        )

        # URLs for the views
        self.password_change_url = reverse("password_change")
        self.password_change_done_url = reverse("password_change_done")

    def test_password_change_template(self):
        """Test that the password_change view uses the correct template"""
        self.client.force_login(user=self.user)
        response = self.client.get(self.password_change_url)
        self.assertTemplateUsed(response, "authentication/password_change.html")

    def test_password_change_success_url(self):
        """Test that the success_url for password_change redirects to the correct URL"""
        self.client.force_login(user=self.user)

        # Prepare new password data
        data = {
            "old_password": "testpassword",
            "new_password1": "newpassword123",
            "new_password2": "newpassword123",
        }

        # Perform password change
        response = self.client.post(self.password_change_url, data)

        # Check if redirected to success URL
        self.assertRedirects(response, self.password_change_done_url)

    def test_password_change_done_template(self):
        """Test that the password_change_done view uses the correct template"""
        self.client.force_login(user=self.user)
        response = self.client.get(self.password_change_done_url)
        self.assertTemplateUsed(response, "authentication/password_change_done.html")

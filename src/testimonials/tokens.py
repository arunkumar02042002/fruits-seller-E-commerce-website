from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six


class TokenGenerator(PasswordResetTokenGenerator):
    """Generate a Token for testimonial."""
    def _make_hash_value(self, user, testimonial, timestamp) -> str:
        """Hashed token."""
        return (
            six.text_type(user.pk)
            + six.text_type(timestamp)
            + six.text_type(testimonial.pk)
            + six.text_type(testimonial.status)
        )

testimonial_add_token = TokenGenerator()

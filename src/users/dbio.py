from django.contrib.auth import get_user_model

User = get_user_model()

class UserDBIO():
    """DBIO for User model."""

    @staticmethod
    def get_user_by_email(email):
        """
        Get User by email.
        Returns None if no user exists with the given mail.
        """
        return User.objects.filter(email=email).first()
    
    @staticmethod
    def get_user_by_pk(pk):
        """
        Get User by email.
        Returns None if no user exists with the given mail.
        """
        return User.objects.filter(pk=pk).first()

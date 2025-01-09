import uuid

from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from authentication.choices import UserRoleChoices

from common.utils import GlobalVariable


class CustomUserManager(BaseUserManager):
    """Manager for User Model."""
    def get_queryset(self):
        # Return only non-deleted objects
        return super().get_queryset().filter(deleted_at__isnull=True)

    def save(self, instance, *args, **kwargs):
        """Custom save method to handle created_at and updated_at."""
        user_id = GlobalVariable.get_val('user_id', None)
        if not instance.pk:  # If creating a new instance
            instance.created_by = user_id
        instance.updated_by = user_id
        return super(CustomUserManager, self).save(instance, *args, **kwargs)

    def delete(self, instance, *args, **kwargs):
        """Custom delete method to set deleted_at instead of removing from the database."""
        user_id = GlobalVariable.get_val('user_id', None)
        instance.deleted_at = timezone.now()
        instance.deleted_by = user_id
        instance.save()

    def create_user(self, username, email, password=None, **kwargs):

        if not username:
            raise ValueError("Username can't be None!")

        if not email:
            raise ValueError("Email can't be None!")

        user = self.model(
            email=self.normalize_email(email), username=username, **kwargs
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **kwargs):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
            **kwargs,
        )
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.role = UserRoleChoices.ADMIN

        user.save(using=self._db)
        return user


# Custom User Model
class User(AbstractBaseUser, PermissionsMixin):

    username_validator = UnicodeUsernameValidator()

    uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
        db_index=True,
    )

    first_name = models.CharField(_("first name"), max_length=150, blank=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True)

    email = models.EmailField(_("email address"), unique=True, db_index=True)

    role = models.CharField(
        max_length=15, choices=UserRoleChoices.choices, default=UserRoleChoices.USER
    )

    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )

    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Created At'
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Last Updated At'
    )

    deleted_at = models.DateTimeField(
        null=True, blank=True,
        verbose_name='Deleted At'
    )

    created_by = models.ForeignKey(
        'User',
        related_name='created_%(class)s_set',
        null=True, blank=True,
        verbose_name='Created By',
        on_delete=models.SET_NULL
    )
    updated_by = models.ForeignKey(
        'User',
        related_name='updated_%(class)s_set',
        null=True, blank=True,
        verbose_name='Updated By',
        on_delete=models.SET_NULL
    )
    deleted_by = models.ForeignKey(
        'User',
        related_name='deleted_%(class)s_set',
        null=True, blank=True,
        verbose_name='Deleted By',
        on_delete=models.SET_NULL
    )

    objects = CustomUserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

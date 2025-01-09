import uuid

from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

from .utils import GlobalVariable

User = get_user_model()

# Create your models here.
class CustomManager():

    def get_queryset(self):
        # Return only non-deleted objects
        return super().get_queryset().filter(deleted_at__isnull=True)

    def save(self, instance, *args, **kwargs):
        """Custom save method to handle created_at and updated_at."""
        user_id = GlobalVariable.get_val('user_id', None)
        if not instance.pk:  # If creating a new instance
            instance.created_at = timezone.now()
            instance.created_by = user_id
        instance.updated_at = timezone.now()
        instance.updated_by = user_id
        return super(CustomManager, self).save(instance, *args, **kwargs)

    def delete(self, instance, *args, **kwargs):
        """Custom delete method to set deleted_at instead of removing from the database."""
        user_id = GlobalVariable.get_val('user_id', None)
        instance.deleted_at = timezone.now()
        instance.deleted_by = user_id
        instance.save()


class PrimaryAuditModel(models.Model):
    """Sets uuid as primary key and adds a custom manager."""

    uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    objects = CustomManager()

    class Meta:
        abstract = True


class TimeStampedModel(models.Model):
    """Tracks when was the object created, updated, and deleted."""

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

    class Meta:
        abstract = True


class UserAuditModel(models.Model):
    """Tracks who created, updated and deleted an instance."""

    created_by = models.ForeignKey(
        User,
        related_name='created_%(class)s_set',
        null=True, blank=True,
        verbose_name='Created By',
        on_delete=models.SET_NULL
    )
    updated_by = models.ForeignKey(
        User,
        related_name='updated_%(class)s_set',
        null=True, blank=True,
        verbose_name='Updated By',
        on_delete=models.SET_NULL
    )
    deleted_by = models.ForeignKey(
        User,
        related_name='deleted_%(class)s_set',
        null=True, blank=True,
        verbose_name='Deleted By',
        on_delete=models.SET_NULL
    )

    class Meta:
        abstract = True


class BaseModel(PrimaryAuditModel, UserAuditModel, TimeStampedModel):
    """Every model must inherit from BaseModel"""

    class Meta:
        abstract = True
        ordering = '-created_at',

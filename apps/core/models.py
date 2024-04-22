from django.db import models
from apps.core.managers import LogicalManager


class TimeStampMixin(models.Model):
    create_at = models.DateTimeField(auto_now_add=True, editable=False)
    modify_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        abstract = True


class LogicalMixin(models.Model):
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    objects = LogicalManager()

    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.save(update_fields=["is_deleted"])

    def deactivate(self):
        self.is_active = False
        self.save(update_fields=["is_active"])

    class Meta:
        abstract = True

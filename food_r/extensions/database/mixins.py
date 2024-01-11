from django.db import models
from django.utils import timezone


class TimestampMixin(models.Model):
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(null=True)

    def save(self, *args, **kwargs):
        if self.pk:
            self.updated = timezone.now()
        super().save(*args, **kwargs)

    class Meta:
        abstract = True

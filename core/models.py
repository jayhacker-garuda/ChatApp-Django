from django.db import models
import uuid


class BaseModel(models.Model):
    uid = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True
    )

    created_at = models.DateTimeField(auto_now=True, blank=True)
    updated_at = models.DateTimeField(auto_now_add=True, blank=True)

    class Meta:
        abstract = True

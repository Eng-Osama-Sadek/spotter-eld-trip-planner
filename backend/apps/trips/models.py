from django.db import models
import uuid


class Trip(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    current_location = models.CharField(max_length=255)
    pickup_location = models.CharField(max_length=255)
    dropoff_location = models.CharField(max_length=255)
    cycle_used_hours = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    result_json = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ["-created_at"]

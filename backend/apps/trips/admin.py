from django.contrib import admin
from .models import Trip


@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ("current_location", "pickup_location", "dropoff_location", "cycle_used_hours", "created_at")

from django.urls import path
from .views import PlanTripView

urlpatterns = [
    path("plan/", PlanTripView.as_view(), name="plan-trip"),
]

"""
URL mappings for the teams app.
"""

from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter

from teams import views

router = DefaultRouter()
router.register("teams", views.TeamViewSet)

app_name = "teams"

urlpatterns = [
    path("", include(router.urls)),
]

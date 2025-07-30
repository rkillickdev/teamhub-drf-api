"""
views for the teams APIs.
"""

from rest_framework import viewsets
from users.authentication import CustomJWTAuthentication
from rest_framework.permissions import IsAuthenticated

from teams.models import Team
from teams import serializers


class TeamViewSet(viewsets.ModelViewSet):
    """View for manage teams APIs."""

    serializer_class = serializers.TeamSerializer
    queryset = Team.objects.all()
    # authentication_classes = [CustomJWTAuthentication]
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve teams for authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by("-id")

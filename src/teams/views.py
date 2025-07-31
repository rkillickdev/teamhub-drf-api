"""
views for the teams APIs.
"""

from rest_framework import viewsets, mixins
from users.authentication import CustomJWTAuthentication
from rest_framework.permissions import IsAuthenticated

from .models import Team, Player
from teams import serializers


class TeamViewSet(viewsets.ModelViewSet):
    """View for manage teams APIs."""

    serializer_class = serializers.TeamDetailSerializer
    queryset = Team.objects.all()
    # authentication_classes = [CustomJWTAuthentication]
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve teams for authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by("-id")

    def get_serializer_class(self):
        """Return the serializer class for request"."""
        if self.action == "list":
            return serializers.TeamSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new team."""
        serializer.save(user=self.request.user)


class PlayerViewSet(
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    """Manage players in the database."""

    serializer_class = serializers.PlayerSerializer
    queryset = Player.objects.all()
    # authentication_classes = [CustomJWTAuthentication]
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter queryset to authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by(
            "-last_name"
        )

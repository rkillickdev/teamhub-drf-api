"""
views for the teams APIs.
"""

from django.db.models import Count, Q
from rest_framework import viewsets, mixins
from users.authentication import CustomJWTAuthentication
from rest_framework.permissions import IsAuthenticated

from .models import League, Team, Player, Match
from teams import serializers
from app.permissions import IsStaffUser, IsOwnerOrReadOnly


class LeagueViewSet(viewsets.ModelViewSet):
    """View for manage leagues APIs."""

    serializer_class = serializers.LeagueSerializer
    queryset = League.objects.all()
    permission_classes = [IsStaffUser]

    def get_queryset(self):
        """Filter leagues to match the age_group and category of teams owned by the authenticated user."""
        user_teams = Team.objects.filter(user=self.request.user)
        age_groups = user_teams.values_list("age_group", flat=True)
        categories = user_teams.values_list("category", flat=True)
        return self.queryset.filter(
            age_group__in=age_groups, category__in=categories
        )


class TeamViewSet(viewsets.ModelViewSet):
    """View for manage teams APIs."""

    serializer_class = serializers.TeamDetailSerializer
    queryset = Team.objects.all()
    permission_classes = [IsAuthenticated and IsOwnerOrReadOnly]

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
        """Filter queryset to players linked to teams owned by the authenticated user."""
        return self.queryset.filter(team__user=self.request.user).order_by(
            "-last_name"
        )


class MatchViewSet(viewsets.ModelViewSet):
    """Manage matches in the database"""

    serializer_class = serializers.MatchSerializer
    queryset = Match.objects.all()

    def get_queryset(self):
        """Filter queryset to matches related to teams owned by the authenticated user."""
        return self.queryset.filter(team__user=self.request.user).order_by(
            "date"
        )

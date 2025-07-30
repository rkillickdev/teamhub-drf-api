"""
Serializers for teams APIs
"""

from rest_framework import serializers

from teams.models import Team


class TeamSerializer(serializers.ModelSerializer):
    """Serializer for teams."""

    class Meta:
        model = Team
        fields = [
            "id",
            "name",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id"]


class TeamDetailSerializer(TeamSerializer):
    """Serializer for teams detail view."""

    class Meta(TeamSerializer.Meta):
        fields = TeamSerializer.Meta.fields + ["manager"]

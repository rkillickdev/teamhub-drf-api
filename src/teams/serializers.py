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
            "manager",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id"]

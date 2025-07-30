"""
Serializers for teams APIs
"""

from rest_framework import serializers

from .models import Team, Player


class PlayerSerializer(serializers.ModelSerializer):
    """Serializer for players."""

    class Meta:
        model = Player
        fields = [
            "id",
            "first_name",
            "last_name",
        ]
        read_only_fields = ["id"]


class TeamSerializer(serializers.ModelSerializer):
    """Serializer for teams."""

    players = PlayerSerializer(many=True, required=False)

    class Meta:
        model = Team
        fields = [
            "id",
            "name",
            "created_at",
            "updated_at",
            "players",
        ]
        read_only_fields = ["id"]

    def create(self, validated_data):
        """Create a player."""
        players = validated_data.pop("players", [])
        team = Team.objects.create(**validated_data)
        auth_user = self.context["request"].user
        for player in players:
            player_obj, created = Player.objects.get_or_create(
                user=auth_user,
                **player,
            )
            team.players.add(player_obj)

        return team


class TeamDetailSerializer(TeamSerializer):
    """Serializer for teams detail view."""

    class Meta(TeamSerializer.Meta):
        fields = TeamSerializer.Meta.fields + ["manager"]

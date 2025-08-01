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

    owner = serializers.ReadOnlyField(source="user.first_name")
    is_owner = serializers.SerializerMethodField()
    players = PlayerSerializer(many=True, required=False)
    player_count = serializers.SerializerMethodField()

    def get_is_owner(self, obj):
        request = self.context["request"]
        return request.user == obj.user

    def get_player_count(self, obj):
        return obj.players.count()

    class Meta:
        model = Team
        fields = [
            "id",
            "owner",
            "is_owner",
            "name",
            "created_at",
            "updated_at",
            "players",
            "player_count",
        ]
        read_only_fields = ["id"]

    def _get_or_create_players(self, players, team):
        """Handle getting or creating players as needed."""
        auth_user = self.context["request"].user
        for player in players:
            player_obj, created = Player.objects.get_or_create(
                user=auth_user,
                **player,
            )
            team.players.add(player_obj)

    def create(self, validated_data):
        """Create a team."""
        players = validated_data.pop("players", [])
        team = Team.objects.create(**validated_data)
        self._get_or_create_players(players, team)

        return team

    def update(self, instance, validated_data):
        """Update a team"""
        players = validated_data.pop("players", None)
        if players is not None:
            instance.players.clear()
            self._get_or_create_players(players, instance)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class TeamDetailSerializer(TeamSerializer):
    """Serializer for teams detail view."""

    class Meta(TeamSerializer.Meta):
        fields = TeamSerializer.Meta.fields + ["manager"]

from rest_framework import serializers
from teams.serializers import TeamSerializer

from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    """Serializer for profiles."""

    teams = TeamSerializer(many=True, required=False)

    class Meta:
        model = Profile
        fields = ["id", "teams", "approved"]
        read_only_fields = ["id"]

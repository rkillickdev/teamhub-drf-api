from rest_framework import viewsets

from profiles import serializers
from .models import Profile


class ProfileViewSet(viewsets.ModelViewSet):
    """View for manage leagues APIs."""

    serializer_class = serializers.ProfileSerializer
    queryset = Profile.objects.all()
    # permission_classes = [IsStaffUser]

    def get_queryset(self):
        """Retrieve profile for authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by("-id")

    def perform_create(self, serializer):
        """Create a new profile"""
        serializer.save(user=self.request.user)

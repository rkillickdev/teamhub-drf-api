from django.db import models
from django.conf import settings
from teams.models import Team


class Profile(models.Model):
    """Profile Model.  Related to a User instance via a One To One Field."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    teams = models.ManyToManyField(Team, related_name="profiles", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.last_name}, {self.user.first_name}"

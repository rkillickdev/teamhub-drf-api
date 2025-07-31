from django.conf import settings
from django.db import models


class Team(models.Model):
    """Team object"""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=255)
    manager = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    players = models.ManyToManyField("Player")

    def __str__(self):
        return self.name


class Player(models.Model):
    """Player object"""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Opponent(models.Model):
    """Opponent object"""

    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Match(models.Model):
    """Match object"""

    HOME = "home"
    AWAY = "away"
    MATCH_TYPE_CHOICES = [
        (HOME, "Home"),
        (AWAY, "Away"),
    ]

    team = models.ForeignKey(
        Team,
        related_name="matches",
        on_delete=models.CASCADE,
    )
    opponent = models.ForeignKey(
        Opponent,
        related_name="matches",
        on_delete=models.CASCADE,
    )
    match_type = models.CharField(
        max_length=10,
        choices=MATCH_TYPE_CHOICES,
        default=HOME,
    )
    date = models.DateTimeField()
    team_score = models.PositiveIntegerField(default=0)
    opponent_score = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.team.name} ({self.get_match_type_display()}) vs {self.opponent.name} on {self.date}"


class Goal(models.Model):
    """Goal object"""

    match = models.ForeignKey(
        Match,
        related_name="goals",
        on_delete=models.CASCADE,
    )
    player = models.ForeignKey(
        Player,
        related_name="goals",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    team = models.ForeignKey(
        Team,
        related_name="goals",
        on_delete=models.CASCADE,
    )
    is_opponent_goal = models.BooleanField(default=False)
    time_scored = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.is_opponent_goal:
            return f"Goal by opponent in match {self.match}"
        return (
            f"Goal by {self.player} for {self.team.name} in match {self.match}"
        )

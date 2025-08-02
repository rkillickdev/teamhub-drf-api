from django.conf import settings
from django.db import models


U8 = "U8"
U9 = "U9"

AGE_BRACKET_CHOICES = [
    (U8, "Under 8"),
    (U9, "Under 9"),
]

MALE = "MALE"
FEMALE = "FEMALE"
MIXED = "MIXED"

CATEGORY_CHOICES = [
    (MALE, "Male"),
    (FEMALE, "Female"),
    (MIXED, "Mixed"),
]


class League(models.Model):
    """League object"""

    name = models.CharField(max_length=255)
    age_group = models.CharField(max_length=10, choices=AGE_BRACKET_CHOICES)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)

    def __str__(self):
        return f"{self.name}.  {self.age_group}.  {self.category}"


class Team(models.Model):
    """Team object"""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=255)
    age_group = models.CharField(max_length=10, choices=AGE_BRACKET_CHOICES)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    league = models.ForeignKey(
        League,
        null=True,
        blank=True,
        related_name="teams",
        on_delete=models.CASCADE,
    )
    manager = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    players = models.ManyToManyField(
        "Player", related_name="teams", blank=True
    )

    def __str__(self):
        return self.name


class Player(models.Model):
    """Player object"""

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


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
    opponent = models.ForeignKey(Team, on_delete=models.CASCADE)
    match_type = models.CharField(
        max_length=10,
        choices=MATCH_TYPE_CHOICES,
        default=HOME,
    )
    date = models.DateTimeField()
    team_score = models.PositiveIntegerField(default=0)
    opponent_score = models.PositiveIntegerField(default=0)
    match_complete = models.BooleanField(default=False)
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

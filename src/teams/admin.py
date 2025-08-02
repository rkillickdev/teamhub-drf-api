from django.contrib import admin
from .models import League, Team, Player, Match, Goal

admin.site.register(League)
admin.site.register(Team)
admin.site.register(Player)
admin.site.register(Match)
admin.site.register(Goal)

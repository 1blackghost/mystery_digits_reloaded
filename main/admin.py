from django.contrib import admin
from .models import UserProfile

admin.site.register(UserProfile)
from .models import leaderboard

admin.site.register(leaderboard)
from django.contrib import admin
from .models import PlayLog

@admin.register(PlayLog)
class PlayLogAdmin(admin.ModelAdmin):
    list_display = ('contract', 'played_at', 'duration')
    readonly_fields = ('played_at',)

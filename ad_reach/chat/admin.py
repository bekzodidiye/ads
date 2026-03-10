from django.contrib import admin
from .models import Message

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('contract', 'sender', 'text', 'created_at', 'is_read')
    list_filter = ('is_read',)
    readonly_fields = ('created_at',)

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

from django.contrib import admin
from .models import Contract

@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = ('id', 'advertiser', 'monitor', 'total_amount', 'status', 'is_ai_verified', 'created_at')
    list_filter = ('status', 'is_ai_verified')
    search_fields = ('advertiser__phone', 'monitor__title')
    readonly_fields = ('created_at',)

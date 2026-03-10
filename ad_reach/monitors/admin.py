from django.contrib import admin
from .models import Monitor, Slot

@admin.register(Monitor)
class MonitorAdmin(admin.ModelAdmin):
    list_display = ('title', 'vendor', 'price_per_slot', 'is_active', 'resolution')
    list_filter = ('is_active',)
    search_fields = ('title', 'vendor__phone', 'vendor__full_name')

@admin.register(Slot)
class SlotAdmin(admin.ModelAdmin):
    list_display = ('monitor', 'start_time', 'end_time', 'is_booked')
    list_filter = ('is_booked',)

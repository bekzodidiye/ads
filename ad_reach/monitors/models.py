from django.db import models
from django.conf import settings

class Monitor(models.Model):
    vendor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='monitors')
    title = models.CharField(max_length=255)
    lat = models.DecimalField(max_digits=10, decimal_places=8)
    lng = models.DecimalField(max_digits=11, decimal_places=8)
    resolution = models.CharField(max_length=50) # e.g., "1920x1080"
    price_per_slot = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class Slot(models.Model):
    monitor = models.ForeignKey(Monitor, on_delete=models.CASCADE, related_name='slots')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_booked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.monitor.title} | {self.start_time} - {self.end_time}"


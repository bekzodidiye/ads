from django.db import models
from django.conf import settings
from monitors.models import Monitor
from django.core.validators import FileExtensionValidator

class Contract(models.Model):
    STATUS_CHOICES = (
        ('pending', 'kutilmoqda'),
        ('active', 'faol'),
        ('completed', 'tugallandi'),
        ('cancelled', 'bekor qilindi'),
    )

    advertiser = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='contracts')
    monitor = models.ForeignKey(Monitor, on_delete=models.CASCADE, related_name='contracts')
    video_file = models.FileField(
        upload_to='videos/',
        validators=[FileExtensionValidator(allowed_extensions=['mp4', 'mov'])]
    )
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    is_ai_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Contract {self.id} - {self.advertiser.phone} on {self.monitor.title}"

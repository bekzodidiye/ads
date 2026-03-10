from django.db import models
from django.conf import settings
from contracts.models import Contract
from django.core.exceptions import PermissionDenied
from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver

class Message(models.Model):
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='messages')
    text = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Msg from {self.sender.phone} in Contract {self.contract.id}"

@receiver(pre_delete, sender=Message)
def prevent_message_deletion(sender, instance, **kwargs):
    raise PermissionDenied("Messages cannot be deleted.")

@receiver(pre_save, sender=Message)
def prevent_message_update(sender, instance, **kwargs):
    if instance.pk:
        orig = Message.objects.get(pk=instance.pk)
        if orig.text != instance.text or orig.sender != instance.sender or True: # block any update to core content
            if orig.is_read != instance.is_read:
                 pass # allow updating read status
            else:
                 raise PermissionDenied("Messages cannot be updated.")


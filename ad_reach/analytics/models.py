from django.db import models
from contracts.models import Contract

class PlayLog(models.Model):
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, related_name='play_logs')
    played_at = models.DateTimeField(auto_now_add=True)
    duration = models.IntegerField(help_text="Duration in seconds")
    
    def __str__(self):
        return f"Log for Contract {self.contract_id} at {self.played_at}"


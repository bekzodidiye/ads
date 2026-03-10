from rest_framework import serializers
from .models import PlayLog

class PlayLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayLog
        fields = '__all__'

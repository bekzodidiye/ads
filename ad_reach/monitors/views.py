from rest_framework import viewsets, permissions, generics
from rest_framework.response import Response
from .models import Monitor, Slot
from .serializers import MonitorSerializer
from contracts.models import Contract
from django.utils import timezone
import logging

logger = logging.getLogger('finance')

from drf_spectacular.utils import extend_schema

@extend_schema(tags=['Monitors'])
class MonitorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Monitor.objects.filter(is_active=True)
    serializer_class = MonitorSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = super().get_queryset()
        
        city = self.request.query_params.get('city')
        # Simple geographic filtering is requested, normally PostGIS is needed 
        # but for this PRD we'll assume filtering based on a field if added or skip if lat/lang only.
        # Since 'city' isn't in the model, we filter by price below:
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')

        if min_price:
            queryset = queryset.filter(price_per_slot__gte=min_price)
        if max_price:
            queryset = queryset.filter(price_per_slot__lte=max_price)
            
        return queryset

class PlayerPlaylistView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        # In a real scenario, we'd identify the monitor by an API Key or ID passed in params
        monitor_id = request.query_params.get('monitor_id')
        if not monitor_id:
            return Response({"error": "monitor_id required"}, status=400)
            
        now = timezone.now()
        # Find active contracts for this monitor for the current time
        # This is simplified: in reality we'd check if 'now' is within scheduled slots
        contracts = Contract.objects.filter(
            monitor_id=monitor_id, 
            status='active'
        )
        
        playlist = []
        for c in contracts:
            playlist.append({
                "contract_id": c.id,
                "video_url": request.build_absolute_uri(c.video_file.url)
            })
            
        return Response({"playlist": playlist})

class PlayerPingView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        monitor_id = request.data.get('monitor_id')
        logger.info(f"Player Ping received for monitor {monitor_id}")
        return Response({"status": "pong"})

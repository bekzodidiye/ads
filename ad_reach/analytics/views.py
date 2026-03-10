from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import PlayLog
from .serializers import PlayLogSerializer
from contracts.models import Contract

class PlayLogCreateView(generics.CreateAPIView):
    queryset = PlayLog.objects.all()
    serializer_class = PlayLogSerializer
    permission_classes = [permissions.AllowAny] # Player app uses this

class AnalyticsReportView(generics.RetrieveAPIView):
    queryset = Contract.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        contract = self.get_object()
        logs = PlayLog.objects.filter(contract=contract)
        
        report_data = {
            "contract_id": contract.id,
            "total_plays": logs.count(),
            "is_ai_verified": contract.is_ai_verified,
            "status": contract.status,
            "created_at": contract.created_at
        }
        return Response(report_data)

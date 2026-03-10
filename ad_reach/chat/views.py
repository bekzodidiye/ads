from rest_framework import generics, permissions
from .models import Message
from .serializers import MessageSerializer
from contracts.models import Contract

class MessageListCreateView(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        contract_id = self.kwargs.get('contract_id')
        return Message.objects.filter(contract_id=contract_id)

    def perform_create(self, serializer):
        contract_id = self.kwargs.get('contract_id')
        contract = Contract.objects.get(id=contract_id)
        serializer.save(sender=self.request.user, contract=contract)

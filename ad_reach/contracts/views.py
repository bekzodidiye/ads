from rest_framework import generics, permissions, status, serializers
from rest_framework.response import Response
from .models import Contract
from .serializers import ContractSerializer
from django.db import transaction

from drf_spectacular.utils import extend_schema

@extend_schema(tags=['Contracts'])
class ContractCreateView(generics.CreateAPIView):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        if user.role != 'advertiser':
            raise serializers.ValidationError("Only advertisers can create contracts.")
            
        monitor = serializer.validated_data['monitor']
        total_amount = serializer.validated_data['total_amount']
        
        with transaction.atomic():
            # Refresh user from db to get latest balance
            user.refresh_from_db()
            
            if user.balance < total_amount:
                raise serializers.ValidationError({"error": "Insufficient balance."})
                
            user.balance -= total_amount
            user.frozen_balance += total_amount
            user.save(update_fields=['balance', 'frozen_balance'])
            
            serializer.save(advertiser=user, status='active')

@extend_schema(tags=['Contracts'])
class MyAdsListView(generics.ListAPIView):
    serializer_class = ContractSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'advertiser':
            return Contract.objects.filter(advertiser=user)
        elif user.role == 'vendor':
            return Contract.objects.filter(monitor__vendor=user)
        return Contract.objects.none()

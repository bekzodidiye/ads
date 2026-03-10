from celery import shared_task
from .models import Contract
from analytics.models import PlayLog
from django.db import transaction
from django.utils import timezone
import logging

logger = logging.getLogger('finance')

@shared_task
def check_expired_contracts():
    # This would be called by celery beat periodically
    # Check for contracts that should have ended and trigger verification
    active_contracts = Contract.objects.filter(status='active')
    for contract in active_contracts:
        # For simplicity, we assume verification happens after some time
        # In real case, we'd check against Slot end_times
        verify_contract_completion.delay(contract.id)

@shared_task
def verify_contract_completion(contract_id):
    try:
        with transaction.atomic():
            contract = Contract.objects.select_for_update().get(id=contract_id)
            if contract.status != 'active':
                return
            
            # AI Logic: Proof of Play verification
            logs_count = PlayLog.objects.filter(contract=contract).count()
            # Simplified threshold: let's say 10 logs for '95%' success in this demo
            if logs_count >= 10:
                contract.is_ai_verified = True
                
            if contract.is_ai_verified:
                # Platform takes 10%
                platform_fee = contract.total_amount * 0.1
                vendor_amount = contract.total_amount - platform_fee
                
                vendor = contract.monitor.vendor
                vendor.balance += vendor_amount
                vendor.save()
                
                advertiser = contract.advertiser
                advertiser.frozen_balance -= contract.total_amount
                advertiser.save()
                
                contract.status = 'completed'
                logger.info(f"Contract {contract.id} completed. Fee: {platform_fee}, Vendor: {vendor_amount}")
            else:
                # Refund to advertiser
                advertiser = contract.advertiser
                advertiser.balance += contract.total_amount
                advertiser.frozen_balance -= contract.total_amount
                advertiser.save()
                
                contract.status = 'cancelled'
                logger.info(f"Contract {contract.id} failed verification. Refunded {contract.total_amount}")
                
            contract.save()
    except Contract.DoesNotExist:
        pass

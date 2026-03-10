from django.urls import path
from .views import ContractCreateView, MyAdsListView

urlpatterns = [
    path('create/', ContractCreateView.as_view(), name='contract-create'),
    path('my-ads/', MyAdsListView.as_view(), name='my-ads'),
]

from django.urls import path
from .views import MessageListCreateView

urlpatterns = [
    path('<int:contract_id>/', MessageListCreateView.as_view(), name='chat-messages'),
]

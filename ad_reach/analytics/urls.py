from django.urls import path
from .views import PlayLogCreateView, AnalyticsReportView

urlpatterns = [
    path('log/', PlayLogCreateView.as_view(), name='play-log-create'),
    path('report/<int:pk>/', AnalyticsReportView.as_view(), name='analytics-report'),
]

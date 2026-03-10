from django.urls import path
from .views import PlayerPlaylistView, PlayerPingView

urlpatterns = [
    path('playlist/', PlayerPlaylistView.as_view(), name='player-playlist'),
    path('ping/', PlayerPingView.as_view(), name='player-ping'),
]

from django.urls import path

from matches.views import (
    ImportLeagueView,
    PlayerListAPIView,
    TeamRetrieveAPIView,
)

urlpatterns = [
    path('importLeague/<slug:code>/', ImportLeagueView.as_view(), name='import'),

    # API
    path('players/<slug:code>/', PlayerListAPIView.as_view()),
    path('team/<str:name>/', TeamRetrieveAPIView.as_view()),
]

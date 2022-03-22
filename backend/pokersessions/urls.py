from django.urls import path

from . import views


urlpatterns = [
    path('user/<int:pk>/list/', views.SessionListView.as_view(), name='sessions'),
    path('user/<int:pk>/create/', views.create_session, name='create-session'),
    path('user/<int:pk>/statistics/', views.get_session_statistics, name='session-statistics'),
    path('<int:pk>/', views.SessionDetailsView.as_view(), name='session'),
    path('player-room/<int:room_id>/statistics/', views.get_player_room_statistics, name='room-sessions-statistics'),
]

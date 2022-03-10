from django.urls import path

from . import views


urlpatterns = [
    path('list/', views.RoomListView.as_view(), name='rooms'),
    path('add/', views.RoomDetailView.as_view(), name='add'),
    path('player/room/list/', views.get_player_rooms, name='player-rooms'),
    path('<int:pk>/', views.RoomDetailView.as_view(), name='room'),
    path('<int:pk>/players/', views.get_room_players, name='room-players'),
    path('<int:pk>/delete/', views.delete_room, name='delete-room'),
]

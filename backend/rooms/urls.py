from django.urls import path

from . import views


urlpatterns = [
    path('list/', views.RoomListView.as_view(), name='rooms'),
    path('add/', views.RoomDetailView.as_view(), name='add'),
    path('player/room/user/<int:pk>/list/', views.get_player_rooms, name='player-rooms'),
    path('player/room/<int:pk>/', views.PlayerRoomDetailView.as_view(), name='player-room'),
    path('<int:pk>/', views.RoomDetailView.as_view(), name='room'),
    path('<int:pk>/players/', views.get_room_players, name='room-players'),
    path('<int:pk>/delete/', views.delete_room, name='delete-room'),
    path('player/<int:pk>/add/player-room/', views.add_player_room, name='add-player-room'),
    path('player/<int:pk>/available/', views.get_available_rooms, name='available-rooms'),
    path('player-room/<int:pk>/delete/', views.delete_player_room, name='delete-player-room'),
    path('player-room/<int:pk>/update/', views.update_player_room, name='update-player-room'),
]

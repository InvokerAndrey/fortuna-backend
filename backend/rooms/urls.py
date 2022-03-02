from django.urls import path

from . import views


urlpatterns = [
    path('list/', views.RoomListView.as_view(), name='rooms'),
    path('<int:pk>/', views.RoomDetailView.as_view(), name='room'),
    path('<int:pk>/players/', views.get_room_players, name='room-players'),
]
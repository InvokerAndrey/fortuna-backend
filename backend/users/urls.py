from django.urls import path

from . import views


urlpatterns = [
    path('login/', views.UserTokenObtainPairView.as_view(), name='login'),
    path('player/register/', views.register_player, name='register-player'),
    path('admin/register/', views.register_admin, name='register-admin'),
    path('admin/list/', views.AdminListView.as_view(), name='admins'),
    path('player/list/', views.PlayerListView.as_view(), name='players'),
    path('player/user/<int:pk>/profile/', views.get_player_profile, name='player-profile'),
    path('player/user/<int:pk>/profile/change-password/', views.change_player_password, name='player-profile'),
    path('player/<int:pk>/', views.PlayerDetailView.as_view(), name='player'),
    path('player/<int:pk>/delete/', views.delete_player, name='delete-player'),
    path('player/<int:pk>/update/', views.update_player_info, name='update-player'),
]

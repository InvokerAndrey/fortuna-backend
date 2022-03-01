from django.urls import path

from . import views


urlpatterns = [
    path('login/', views.UserTokenObtainPairView.as_view(), name='login'),
    path('admin/list/', views.AdminListView.as_view(), name='admins'),
    path('player/list/', views.PlayerListView.as_view(), name='players'),
    path('player/<int:pk>/', views.PlayerDetailView.as_view(), name='player'),
]

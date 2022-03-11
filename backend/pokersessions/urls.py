from django.urls import path

from . import views


urlpatterns = [
    path('list/', views.SessionListView.as_view(), name='sessions'),
    path('<int:pk>/', views.SessionDetailsView.as_view(), name='session'),
]

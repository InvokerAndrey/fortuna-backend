from django.urls import path

from . import views


urlpatterns = [
    path('list/', views.SessionListView.as_view(), name='sessions'),
    path('create/', views.create_session, name='create-session'),
    path('<int:pk>/', views.SessionDetailsView.as_view(), name='session'),
]

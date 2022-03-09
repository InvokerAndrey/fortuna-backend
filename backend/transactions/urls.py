from django.urls import path

from . import views


urlpatterns = [
    path('add/player-transaction/<int:pk>/', views.add_player_transaction, name='add-player-transaction')
]

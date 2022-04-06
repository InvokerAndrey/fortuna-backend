from django.urls import path

from . import views


urlpatterns = [
    path('fund-transactions/', views.FundTransactionListView.as_view(), name='fund-transactions'),
    path('player/user/<int:pk>/room-transaction/list/', views.RoomTransactionListView.as_view(), name='room-transactions'),
    path('player/room-transaction/add/', views.add_room_transaction, name='add-room-transaction'),
    path('player/user/<int:pk>/player-transaction/list/', views.PlayerTransactionListView.as_view(), name='player-transactions'),
    path('add/player-transaction/', views.add_player_transaction, name='add-player-transaction'),
    path('add/fund-transaction/', views.add_fund_transaction, name='add-fund-transaction'),
    path('player/<int:pk>/player-transactions/', views.get_player_player_transactions, name='player-player-transactions'),
    path('player/<int:pk>/room-transactions/', views.get_player_room_transactions, name='player-room-transactions'),
]

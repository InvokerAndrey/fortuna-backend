from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from .serializers import (
    PlayerTransactionSerializer,
    RoomTransactionSerializer,
    GetPlayerTransactionsSerializer,
    GetRoomTransactionsSerializer
)
from .models import RoomTransaction, PlayerTransaction
from .enums import RoomTransactionSortEnum
from users.models import Player
from core.views import BaseListView, Pagination


@api_view(['POST'])
@permission_classes([IsAdminUser])
def add_player_transaction(request):
    context = {
        'player_id': request.data['player_id'],
        'admin_user': request.user
    }
    serializer = PlayerTransactionSerializer(data=request.data, context=context)
    if serializer.is_valid():
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)
    return Response({'detail': '\n'.join(serializer.errors['non_field_errors'])}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_room_transaction(request):
    context = {
        'player': request.user.player,
        'player_room_id': request.data['player_room_id']
    }
    serializer = RoomTransactionSerializer(data=request.data, context=context)
    if serializer.is_valid():
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)
    return Response({'detail': '\n'.join(serializer.errors['non_field_errors'])}, status=status.HTTP_400_BAD_REQUEST)


class RoomTransactionListView(BaseListView):
    def get(self, request):
        params = request.query_params
        print(params)
        sort_field = params.get('sort') or None
        if sort_field:
            sort_param = RoomTransactionSortEnum.get_sort_by_field(sort_field)
            transaction_qs = RoomTransaction.objects.all().order_by(sort_param)
        else:
            transaction_qs = RoomTransaction.objects.all()
        paginator = Pagination()
        page = paginator.paginate_queryset(transaction_qs, request)
        serializer = RoomTransactionSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)


class PlayerTransactionListView(BaseListView):
    model = PlayerTransaction
    serializer_class = PlayerTransactionSerializer


@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_player_player_transactions(request, pk):
    paginator = Pagination()
    player = Player.objects.get(pk=pk)
    player_transactions = PlayerTransaction.objects.filter(player=player)
    page = paginator.paginate_queryset(player_transactions, request)
    serializer = GetPlayerTransactionsSerializer(page, many=True)
    return paginator.get_paginated_response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_player_room_transactions(request, pk):
    paginator = Pagination()
    player = Player.objects.get(pk=pk)
    room_transactions = RoomTransaction.objects.filter(player=player)
    page = paginator.paginate_queryset(room_transactions, request)
    serializer = GetRoomTransactionsSerializer(page, many=True)
    return paginator.get_paginated_response(serializer.data)

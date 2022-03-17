from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from dateutil.parser import parse

from .serializers import (
    PlayerTransactionSerializer,
    RoomTransactionSerializer,
    GetPlayerTransactionsSerializer,
    GetRoomTransactionsSerializer
)
from .models import RoomTransaction, PlayerTransaction
from .enums import RoomTransactionTypeEnum
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
        start_date = None
        end_date = None

        if params.get('start_date'):
            try:
                start_date = parse(params.get('start_date'))
                print(start_date)
            except (TypeError, ValueError):
                pass

        if params.get('end_date'):
            try:
                end_date = parse(params.get('end_date'))
                print(end_date)
            except (TypeError, ValueError):
                pass

        if all([start_date, end_date]):
            qs = RoomTransaction.objects.filter(created_at__range=[start_date, end_date])
        elif start_date:
            qs = RoomTransaction.objects.filter(created_at__gte=start_date)
        elif end_date:
            qs = RoomTransaction.objects.filter(created_at__lte=end_date)
        else:
            qs = RoomTransaction.objects.all()

        order = params.get('order')
        if order:
            qs = qs.order_by(params.get('order'), '-pk' if order.startswith('-') else 'pk')
        else:
            qs.order_by('-created_at', '-pk')

        try:
            _type = int(params.get('type'))
            if _type == 0:
                pass
            elif _type in RoomTransactionTypeEnum.values():
                qs = qs.filter(type=_type)
        except (ValueError, TypeError):
            pass

        print('QS', qs)

        paginator = Pagination()
        page = paginator.paginate_queryset(qs, request)
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

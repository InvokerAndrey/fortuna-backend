from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from .serializers import (
    PlayerTransactionSerializer,
    RoomTransactionSerializer,
    FundTransactionSerializer,
)
from .models import RoomTransaction, PlayerTransaction, FundTransaction
from .enums import RoomTransactionTypeEnum, PlayerTransactionTypeEnum, FundTransactionTypeEnum
from .utils import get_transaction_qs, get_fund_transactions_qs
from users.models import User, Fund
from core.views import BaseListView, Pagination


@api_view(['POST'])
@permission_classes([IsAdminUser])
def add_player_transaction(request):
    context = {
        'player_id': request.data['player_id'],
        'admin_user': request.user,
        'fund': Fund.objects.first()
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


@api_view(['POST'])
@permission_classes([IsAdminUser])
def add_fund_transaction(request):
    data = request.data
    data['admin'] = request.user.admin.id
    data['fund'] = request.user.admin.fund.id
    serializer = FundTransactionSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)
    print(serializer.errors)
    return Response({'detail': '\n'.join(serializer.errors['non_field_errors'])}, status=status.HTTP_400_BAD_REQUEST)


class RoomTransactionListView(BaseListView):
    def get(self, request, pk):
        params = request.query_params
        player = User.objects.get(pk=pk).player
        qs = get_transaction_qs(RoomTransaction, RoomTransactionTypeEnum, player, params)
        paginator = Pagination()
        page = paginator.paginate_queryset(qs, request)
        serializer = RoomTransactionSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)


class PlayerTransactionListView(BaseListView):
    def get(self, request, pk):
        params = request.query_params
        player = User.objects.get(pk=pk).player
        qs = get_transaction_qs(PlayerTransaction, PlayerTransactionTypeEnum, player, params)
        paginator = Pagination()
        page = paginator.paginate_queryset(qs, request)
        serializer = PlayerTransactionSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)


class FundTransactionListView(BaseListView):
    def get(self, request):
        params = request.query_params
        fund = Fund.objects.first()
        qs = get_fund_transactions_qs(FundTransaction, FundTransactionTypeEnum, fund, params)
        paginator = Pagination()
        page = paginator.paginate_queryset(qs, request)
        serializer = FundTransactionSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

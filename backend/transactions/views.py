from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from .serializers import PlayerTransactionSerializer, RoomTransactionSerializer
from .models import RoomTransaction, PlayerTransaction
from core.views import BaseListView


@api_view(['POST'])
@permission_classes([IsAdminUser])
def add_player_transaction(request, pk):
    context = {
        'player_id': pk,
        'admin_user': request.user
    }
    serializer = PlayerTransactionSerializer(data=request.data, context=context)
    if serializer.is_valid():
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)
    return Response({'details': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


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
    return Response({'details': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class RoomTransactionListView(BaseListView):
    model = RoomTransaction
    serializer_class = RoomTransactionSerializer


class PlayerTransactionListView(BaseListView):
    model = PlayerTransaction
    serializer_class = PlayerTransactionSerializer

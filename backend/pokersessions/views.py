from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status

from .models import Session, RoomSession
from .serializers import (
    SessionSerializer,
    SessionDetailsSerializer,
    SessionCreateSerializer,
    RoomStatisticsSerializer
)
from .utils import get_session_qs
from core.views import BaseListView, BaseDetailView, Pagination
from rooms.models import PlayerRoom
from users.models import User, Player


class SessionListView(BaseListView):
    def get(self, request, pk):
        player = User.objects.get(pk=pk).player
        params = request.query_params
        qs = get_session_qs(Session, player, params)
        parametrized_profit = sum([session.result for session in qs])
        admin_part = parametrized_profit * (100 - player.rate) / 100 if parametrized_profit > 0 else 0
        player_part = parametrized_profit * player.rate / 100 if parametrized_profit > 0 else 0
        paginator = Pagination()
        page = paginator.paginate_queryset(qs, request)
        serializer = SessionSerializer(page, many=True)
        data = {
            'parametrized_profit': parametrized_profit,
            'admin_part': admin_part,
            'player_part': player_part,
            'sessions': serializer.data,
        }
        return paginator.get_paginated_response(data)


class SessionDetailsView(BaseDetailView):
    model = Session
    serializer_class = SessionDetailsSerializer


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_session(request, pk):
    context = {
        'player': User.objects.get(pk=pk).player,
    }
    serializer = SessionCreateSerializer(data=request.data, context=context)
    if serializer.is_valid():
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)
    return Response({'detail': '\n'.join(serializer.errors['non_field_errors'])}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_player_room_statistics(request, player_id, room_id):
    player = Player.objects.get(pk=player_id)
    player_room = PlayerRoom.objects.get(pk=room_id)
    room_sessions = RoomSession.objects.filter(room=player_room)
    serializer = RoomStatisticsSerializer(room_sessions, many=True)
    data = {
        'full_name': player.user.get_full_name(),
        'room_name': player_room.room.name,
        'statistics': serializer.data
    }
    return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_session_statistics(request, pk):
    player = User.objects.get(pk=pk).player
    sessions = Session.objects.filter(player=player)
    context = {
        'player': player,
    }
    serializer = SessionSerializer(sessions, many=True, context=context)
    return Response(serializer.data)

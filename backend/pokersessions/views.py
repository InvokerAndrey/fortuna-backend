from rest_framework.permissions import IsAuthenticated
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


class SessionListView(BaseListView):
    def get(self, request):
        params = request.query_params
        qs = get_session_qs(Session, params)
        paginator = Pagination()
        page = paginator.paginate_queryset(qs, request)
        serializer = SessionSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)


class SessionDetailsView(BaseDetailView):
    model = Session
    serializer_class = SessionDetailsSerializer


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_session(request):
    context = {
        'player': request.user.player,
    }
    data = request.data
    data['player'] = request.user.player
    serializer = SessionCreateSerializer(data=request.data, context=context)
    if serializer.is_valid():
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)
    return Response({'detail': '\n'.join(serializer.errors['non_field_errors'])}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_player_room_statistics(request, room_id):
    player_room = PlayerRoom(pk=room_id)
    room_sessions = RoomSession.objects.filter(room=player_room)
    serializer = RoomStatisticsSerializer(room_sessions, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_session_statistics(request):
    player = request.user.player
    sessions = Session.objects.filter(player=player)
    serializer = SessionSerializer(sessions, many=True)
    return Response(serializer.data)

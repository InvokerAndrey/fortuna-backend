from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from .models import Room
from .serializers import RoomSerializer
from core.views import BaseListView, BaseDetailView
from users.models import Player
from users.serializers import PlayerListSerializer


class RoomListView(BaseListView):
    model = Room
    serializer_class = RoomSerializer


class RoomDetailView(BaseDetailView):
    model = Room
    serializer_class = RoomSerializer


@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_room_players(request, pk):
    room = get_object_or_404(Room, pk=pk)
    player_ids = room.playerroom_set.values("player")
    players = Player.objects.filter(pk__in=player_ids)
    serializer = PlayerListSerializer(players, many=True)
    return Response(serializer.data)

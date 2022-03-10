from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework import status

from .models import Room, PlayerRoom
from .serializers import RoomSerializer, PlayerRoomSerializer
from core.views import BaseListView, BaseDetailView
from users.models import Player
from users.serializers import PlayerListSerializer


class RoomListView(BaseListView):
    model = Room
    serializer_class = RoomSerializer


class RoomDetailView(BaseDetailView):
    model = Room
    serializer_class = RoomSerializer

    @permission_classes([IsAdminUser])
    def post(self, request):
        data = request.data
        Room.objects.create(
            name=data['name'],
            description=data.get('description'),
            website=data.get('website')
        )
        return Response(status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_room_players(request, pk):
    room = get_object_or_404(Room, pk=pk)
    player_ids = room.playerroom_set.values("player")
    players = Player.objects.filter(pk__in=player_ids)
    serializer = PlayerListSerializer(players, many=True)
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def delete_room(request, pk):
    room = get_object_or_404(Room, pk=pk)
    room.delete()
    return Response(status=status.HTTP_202_ACCEPTED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_player_rooms(request):
    player = request.user.player
    player_rooms = PlayerRoom.objects.filter(player=player)
    serializer = PlayerRoomSerializer(player_rooms, many=True)
    return Response(serializer.data)

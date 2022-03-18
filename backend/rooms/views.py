from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework import status

from .models import Room, PlayerRoom
from .serializers import RoomSerializer, PlayerRoomSerializer, AddPlayerRoomSerializer
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


class PlayerRoomDetailView(BaseDetailView):
    model = PlayerRoom
    serializer_class = PlayerRoomSerializer


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


@api_view(['POST'])
@permission_classes([IsAdminUser])
def add_player_room(request, pk):
    context = {
        'player_id': pk
    }
    serializer = AddPlayerRoomSerializer(data=request.data, context=context)
    if serializer.is_valid():
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)
    return Response({'detail': '\n'.join(serializer.errors['non_field_errors'])}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_available_rooms(request, pk):
    player = Player.objects.get(pk=pk)
    player_rooms = player.playerroom_set.all()
    player_rooms_names = [p_room.room.name for p_room in player_rooms]
    available_rooms = Room.objects.exclude(name__in=player_rooms_names)
    serializer = RoomSerializer(available_rooms, many=True)
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def delete_player_room(request, pk):
    player_room = get_object_or_404(PlayerRoom, pk=pk)
    player_room.delete()
    return Response(status=status.HTTP_202_ACCEPTED)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_player_room(request, pk):
    data = request.data
    player_room = PlayerRoom.objects.get(pk=pk)
    player_room.nickname = data['nickname']
    player_room.save()
    serializer = PlayerRoomSerializer(player_room, many=False)
    return Response(serializer.data)

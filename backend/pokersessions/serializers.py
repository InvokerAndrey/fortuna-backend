from rest_framework import serializers

from .models import Session, RoomSession
from users.serializers import PlayerForSessionSerializer
from rooms.serializers import PlayerRoomSerializer


class SessionSerializer(serializers.ModelSerializer):
    player = PlayerForSessionSerializer()

    class Meta:
        model = Session
        fields = ['id', 'date', 'player']


class RoomSessionSerializer(serializers.ModelSerializer):
    room = PlayerRoomSerializer()

    class Meta:
        model = RoomSession
        fields = ['room', 'balance']


class SessionDetailsSerializer(serializers.ModelSerializer):
    player = PlayerForSessionSerializer()
    room_sessions = serializers.SerializerMethodField()

    def get_room_sessions(self, obj):
        return RoomSessionSerializer(obj.roomsession_set.all(), many=True).data

    class Meta:
        model = Session
        fields = ['id', 'date', 'player', 'room_sessions']

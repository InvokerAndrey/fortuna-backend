from rest_framework import serializers

from .models import Session, RoomSession
from users.serializers import PlayerForSessionSerializer
from rooms.serializers import PlayerRoomSerializer


class SessionSerializer(serializers.ModelSerializer):
    player = PlayerForSessionSerializer()
    result = serializers.SerializerMethodField()

    def get_result(self, obj):
        room_sessions = obj.roomsession_set.all()
        results = [room_session.result for room_session in room_sessions]
        return sum(results)

    class Meta:
        model = Session
        fields = ['id', 'date', 'player', 'result']


class RoomSessionSerializer(serializers.ModelSerializer):
    room = PlayerRoomSerializer()

    class Meta:
        model = RoomSession
        fields = ['id', 'room', 'result']


class SessionDetailsSerializer(serializers.ModelSerializer):
    player = PlayerForSessionSerializer()
    room_sessions = serializers.SerializerMethodField()

    def get_room_sessions(self, obj):
        return RoomSessionSerializer(obj.roomsession_set.all(), many=True).data

    class Meta:
        model = Session
        fields = ['id', 'date', 'player', 'room_sessions']

from rest_framework import serializers
from django.db import IntegrityError

from .models import Session, RoomSession
from users.serializers import PlayerForSessionSerializer
from rooms.serializers import PlayerRoomSerializer
from rooms.models import PlayerRoom


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


class SessionCreateSerializer(serializers.Serializer):
    room_sessions = serializers.ListField()

    def validate(self, data):
        data['player'] = self.context.get('player')
        try:
            for room_session in data['room_sessions']:
                room_session['room'] = PlayerRoom.objects.get(pk=room_session['room_id'])
        except IntegrityError:
            raise serializers.ValidationError('Invalid room')
        return data

    def create(self, validated_data):
        session = Session.objects.create(player=validated_data['player'])
        for room_session in validated_data['room_sessions']:
            RoomSession.objects.create(
                room=room_session['room'],
                session=session,
                result=room_session['result']
            )
        return session

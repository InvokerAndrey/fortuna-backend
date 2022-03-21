from rest_framework import serializers
from django.db import IntegrityError, transaction

from .models import Session, RoomSession
from users.serializers import PlayerForSessionSerializer
from rooms.serializers import PlayerRoomSerializer
from rooms.models import PlayerRoom


class SessionSerializer(serializers.ModelSerializer):
    player = PlayerForSessionSerializer()
    result = serializers.SerializerMethodField()
    profit = serializers.SerializerMethodField()

    def get_result(self, obj):
        room_sessions = obj.roomsession_set.all()
        results = [room_session.result for room_session in room_sessions]
        return sum(results)

    def get_profit(self, obj):
        sessions = Session.objects.filter(pk__lt=obj.pk, created_at__lte=obj.created_at)
        results = [session.result for session in sessions]
        results.append(obj.result)
        return sum(results)

    class Meta:
        model = Session
        fields = ['id', 'created_at', 'player', 'result', 'profit']


class RoomSessionSerializer(serializers.ModelSerializer):
    room = PlayerRoomSerializer()

    class Meta:
        model = RoomSession
        fields = ['id', 'room', 'balance', 'result']


class SessionDetailsSerializer(serializers.ModelSerializer):
    player = PlayerForSessionSerializer()
    room_sessions = serializers.SerializerMethodField()

    def get_room_sessions(self, obj):
        return RoomSessionSerializer(obj.roomsession_set.all(), many=True).data

    class Meta:
        model = Session
        fields = ['id', 'created_at', 'player', 'room_sessions']


class SessionCreateSerializer(serializers.Serializer):
    room_sessions = serializers.ListField()

    def validate(self, data):
        data['player'] = self.context.get('player')

        if len(data['room_sessions']) == 0:
            raise serializers.ValidationError('Add at least one room session')

        room_ids = [room_session['room_id'] for room_session in data['room_sessions']]
        if len(room_ids) > len(set(room_ids)):
            raise serializers.ValidationError('You have added 2 or more sessions for the same room')

        try:
            for room_session in data['room_sessions']:
                room_session['player_room'] = PlayerRoom.objects.get(pk=room_session['room_id'])
                if room_session['balance'] < 0:
                    raise serializers.ValidationError('Room balance cannot be less then 0')
        except IntegrityError:
            raise serializers.ValidationError('Invalid room')

        return data

    @transaction.atomic
    def create(self, validated_data):
        session = Session.objects.create(player=validated_data['player'])
        room_session_results = []
        for room_session in validated_data['room_sessions']:
            room_session_result = room_session['balance'] - room_session['player_room'].balance
            room_session_results.append(room_session_result)
            RoomSession.objects.create(
                room=room_session['player_room'],
                session=session,
                balance=room_session['balance'],
                result=room_session_result
            )
            room_session['player_room'].balance = room_session['balance']
            room_session['player_room'].save()

        session.result = sum(room_session_results)
        session.save()
        return session


class RoomStatisticsSerializer(serializers.ModelSerializer):
    created_at = serializers.DateField(source='session.created_at')
    profit = serializers.SerializerMethodField()

    def get_profit(self, obj):
        sessions = RoomSession.objects.filter(pk__lt=obj.pk)
        results = [session.result for session in sessions]
        results.append(obj.result)
        return sum(results)

    class Meta:
        model = RoomSession
        fields = ['id', 'created_at', 'result', 'profit']

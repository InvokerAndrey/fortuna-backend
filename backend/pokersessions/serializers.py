from rest_framework import serializers
from django.db import IntegrityError, transaction
from decimal import Decimal

from .models import Session, RoomSession
from users.serializers import PlayerForSessionSerializer, PlayerDetailsSerializer
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
        sessions = Session.objects.filter(
            pk__lt=obj.pk,
            created_at__lte=obj.created_at,
            player=self.context.get('player')
        )
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
                if float(room_session['balance']) < 0:
                    raise serializers.ValidationError('Room balance cannot be less then 0')
        except IntegrityError:
            raise serializers.ValidationError('Invalid room')

        return data

    @transaction.atomic
    def create(self, validated_data):
        session = Session.objects.create(player=validated_data['player'])
        room_session_results = []
        for room_session in validated_data['room_sessions']:
            room_session_result = Decimal(room_session['balance']) - Decimal(room_session['player_room'].balance)
            room_session_results.append(room_session_result)
            RoomSession.objects.create(
                room=room_session['player_room'],
                session=session,
                balance=room_session['balance'],
                result=room_session_result,
            )
            room_session['player_room'].balance = room_session['balance']
            room_session['player_room'].save()

        session.result = sum(room_session_results)
        session.save()
        self._update_player(validated_data['player'], session)
        return session

    def _update_player(self, player, session):
        player.all_time_profit += session.result
        player.current_profit += session.result
        serializer = PlayerDetailsSerializer(player, many=False)
        total_rooms_balance = serializer.data['total_rooms_balance']
        total_money = total_rooms_balance + player.balance
        if total_money - player.duty > 0:
            player.admin_profit_share = player.current_profit * (100 - player.rate) / 100
            player.self_profit_share = player.current_profit * player.rate / 100
        else:
            player.admin_profit_share = 0
            player.self_profit_share = 0
        player.save()


class RoomStatisticsSerializer(serializers.ModelSerializer):
    created_at = serializers.DateField(source='session.created_at')
    profit = serializers.SerializerMethodField()
    room_name = serializers.CharField(source='room.room.name')
    full_name = serializers.CharField(source='session.player.user.get_full_name')

    def get_profit(self, obj):
        sessions = RoomSession.objects.filter(pk__lt=obj.pk, room=obj.room)
        results = [session.result for session in sessions]
        results.append(obj.result)
        return sum(results)

    class Meta:
        model = RoomSession
        fields = ['id', 'created_at', 'result', 'profit', 'room_name', 'full_name']

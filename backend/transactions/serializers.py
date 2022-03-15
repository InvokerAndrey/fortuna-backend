from rest_framework import serializers
from django.db import transaction

from .models import PlayerTransaction, RoomTransaction
from .enums import RoomTransactionEnum
from users.models import Player, Admin
from rooms.models import PlayerRoom
from transactions.enums import PlayerTransactionEnum, RoomTransactionEnum


class PlayerTransactionSerializer(serializers.ModelSerializer):
    admin = serializers.SerializerMethodField()

    def get_admin(self, obj):
        return obj.admin.user.get_full_name()

    def validate(self, data):
        if data['amount'] <= 0:
            raise serializers.ValidationError('Нельзя переслать 0 или меньше денег')
        elif not Player.objects.filter(pk=self.context.get('player_id')).exists():
            raise serializers.ValidationError('Нельзя провести транзакцию с несуществующим пользователем')
        elif data['type'] not in PlayerTransactionEnum.values():
            raise serializers.ValidationError('Неверный тип транзакции')

        data['player'] = Player.objects.get(pk=self.context.get('player_id'))
        if data['type'] == PlayerTransactionEnum.PLAYER_TO_ADMIN_PROFIT.value and data['amount'] > data['player'].balance:
            raise serializers.ValidationError('Профит превышает допустимую сумму')

        data['admin'] = self.context.get('admin_user').admin
        return data

    @transaction.atomic
    def create(self, validated_data):
        player_transaction = PlayerTransaction.objects.create(**validated_data)
        if validated_data['type'] == PlayerTransactionEnum.ADMIN_TO_PLAYER_GAME.value:
            transaction.on_commit(
                lambda: self._update_player_balance(validated_data['player'], validated_data['amount'])
            )
        elif validated_data['type'] == PlayerTransactionEnum.PLAYER_TO_ADMIN_PROFIT.value:
            transaction.on_commit(
                lambda: self._update_player_balance(validated_data['player'], -validated_data['amount'])
            )
        return player_transaction

    def _update_player_balance(self, player, amount):
        player.balance += amount
        player.save()

    class Meta:
        model = PlayerTransaction
        fields = ['id', 'type', 'amount', 'admin', 'created_at']


class RoomTransactionSerializer(serializers.ModelSerializer):
    room_name = serializers.SerializerMethodField()

    def get_room_name(self, obj):
        return obj.room.room.name

    def validate(self, data):

        if data['amount'] <= 0:
            raise serializers.ValidationError('Нельзя переслать 0 или меньше денег')
        elif not PlayerRoom.objects.filter(id=self.context.get('player_room_id')).exists():
            raise serializers.ValidationError('Нельзя провести транзакцию с несуществующим румом')
        elif data['type'] not in RoomTransactionEnum.values():
            raise serializers.ValidationError('Неверный тип транзакции')

        data['player'] = self.context.get('player')
        if data['type'] == RoomTransactionEnum.PLAYER_TO_ROOM.value and data['amount'] > data['player'].balance:
            raise serializers.ValidationError('Депозит превышает допустимую сумму')

        data['room'] = PlayerRoom.objects.get(id=self.context.get('player_room_id'))
        return data

    @transaction.atomic
    def create(self, validated_data):
        room_transaction = RoomTransaction.objects.create(**validated_data)
        if validated_data['type'] == RoomTransactionEnum.PLAYER_TO_ROOM.value:
            transaction.on_commit(
                lambda: self._update_room_balance(validated_data['room'], validated_data['amount'])
            )
            transaction.on_commit(
                lambda: self._update_player_balance(validated_data['player'], -validated_data['amount'])
            )
        elif validated_data['type'] == RoomTransactionEnum.ROOM_TO_PLAYER.value:
            transaction.on_commit(
                lambda: self._update_room_balance(validated_data['room'], -validated_data['amount'])
            )
            transaction.on_commit(
                lambda: self._update_player_balance(validated_data['player'], validated_data['amount'])
            )
        return room_transaction

    def _update_room_balance(self, player_room, amount):
        player_room.balance += amount
        player_room.save()

    def _update_player_balance(self, player, amount):
        player.balance += amount
        player.save()

    class Meta:
        model = RoomTransaction
        fields = ['id', 'type', 'amount', 'room_name', 'created_at']


class GetPlayerTransactionsSerializer(serializers.ModelSerializer):
    admin_name = serializers.CharField(source='admin.user.get_full_name')

    class Meta:
        model = PlayerTransaction
        fields = ['id', 'type', 'amount', 'admin_name', 'created_at']


class GetRoomTransactionsSerializer(serializers.ModelSerializer):
    room_name = serializers.CharField(source='room.room.name')

    class Meta:
        model = RoomTransaction
        fields = ['id', 'type', 'amount', 'room_name', 'created_at']

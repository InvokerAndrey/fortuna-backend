from rest_framework import serializers
from django.db import transaction

from .models import PlayerTransaction, RoomTransaction
from .enums import RoomTransactionTypeEnum
from users.models import Player, Admin
from rooms.models import PlayerRoom
from transactions.enums import PlayerTransactionTypeEnum, RoomTransactionTypeEnum


class PlayerTransactionSerializer(serializers.ModelSerializer):
    admin = serializers.SerializerMethodField()

    def get_admin(self, obj):
        return obj.admin.user.get_full_name()

    def validate(self, data):
        if data['amount'] <= 0:
            raise serializers.ValidationError('Cannot send 0 or less money')
        elif not Player.objects.filter(pk=self.context.get('player_id')).exists():
            raise serializers.ValidationError('You cannot make a transaction with a non-existent user')
        elif data['type'] not in PlayerTransactionTypeEnum.values():
            raise serializers.ValidationError('Wrong transaction type')

        data['player'] = Player.objects.get(pk=self.context.get('player_id'))
        if (
            (
                data['type'] == PlayerTransactionTypeEnum.PLAYER_TO_ADMIN_DUTY.value
                or
                data['type'] == PlayerTransactionTypeEnum.PLAYER_TO_ADMIN_PROFIT.value
            )
            and
            data['amount'] > data['player'].balance
        ):
            raise serializers.ValidationError("Amount exceeds player's balance")
        elif (
            data['type'] == PlayerTransactionTypeEnum.PLAYER_TO_ADMIN_DUTY.value
            and
            data['amount'] > data['player'].duty
        ):
            raise serializers.ValidationError("Amount exceeds player's make up")
        elif (
            data['type'] == PlayerTransactionTypeEnum.PLAYER_TO_ADMIN_PROFIT.value
            and
            data['amount'] > data['player'].current_profit
        ):
            raise serializers.ValidationError(f"Profit is {data['player'].current_profit} $")

        data['admin'] = self.context.get('admin_user').admin
        return data

    @transaction.atomic
    def create(self, validated_data):
        player_transaction = PlayerTransaction.objects.create(**validated_data)
        if validated_data['type'] == PlayerTransactionTypeEnum.ADMIN_TO_PLAYER_GAME.value:
            transaction.on_commit(
                lambda: self._update_player_balance(validated_data['player'], validated_data['amount'])
            )
            transaction.on_commit(
                lambda: self._update_player_duty(validated_data['player'], validated_data['amount'])
            )
        elif validated_data['type'] == PlayerTransactionTypeEnum.PLAYER_TO_ADMIN_DUTY.value:
            transaction.on_commit(
                lambda: self._update_player_balance(validated_data['player'], -validated_data['amount'])
            )
            transaction.on_commit(
                lambda: self._update_player_duty(validated_data['player'], -validated_data['amount'])
            )
        elif validated_data['type'] == PlayerTransactionTypeEnum.PLAYER_TO_ADMIN_PROFIT.value:
            transaction.on_commit(
                lambda: self._update_player_balance(validated_data['player'], -validated_data['amount'])
            )
            transaction.on_commit(
                lambda: self._update_player_profit(validated_data['player'], validated_data['amount'])
            )
        return player_transaction

    def _update_player_balance(self, player, amount):
        player.balance += amount
        player.save()

    def _update_player_profit(self, player, amount):
        player.current_profit -= amount
        player.admin_profit_share -= amount * (100 - player.rate) / 100
        player.self_profit_share -= amount * player.rate / 100
        player.profit_to_admin += amount * (100 - player.rate) / 100
        player.salary += amount * player.rate / 100
        player.save()

    def _update_player_duty(self, player, amount):
        player.duty += amount
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
            raise serializers.ValidationError('Cannot send 0 or less money')
        elif not PlayerRoom.objects.filter(id=self.context.get('player_room_id')).exists():
            raise serializers.ValidationError('You cannot make a transaction with a non-existent room')
        elif data['type'] not in RoomTransactionTypeEnum.values():
            raise serializers.ValidationError('Wrong transaction type')

        data['player'] = self.context.get('player')
        if data['type'] == RoomTransactionTypeEnum.DEPOSIT.value and data['amount'] > data['player'].balance:
            raise serializers.ValidationError('Deposit exceeds allowed amount')

        data['room'] = PlayerRoom.objects.get(id=self.context.get('player_room_id'))
        if data['type'] == RoomTransactionTypeEnum.WITHDRAWAL.value and data['room'].balance < data['amount']:
            raise serializers.ValidationError('Withdrawal exceeds allowed amount')
        return data

    @transaction.atomic
    def create(self, validated_data):
        room_transaction = RoomTransaction.objects.create(**validated_data)
        if validated_data['type'] == RoomTransactionTypeEnum.DEPOSIT.value:
            transaction.on_commit(
                lambda: self._update_room_balance(validated_data['room'], validated_data['amount'])
            )
            transaction.on_commit(
                lambda: self._update_player_balance(validated_data['player'], -validated_data['amount'])
            )
        elif validated_data['type'] == RoomTransactionTypeEnum.WITHDRAWAL.value:
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

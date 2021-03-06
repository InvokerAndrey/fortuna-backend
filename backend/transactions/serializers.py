from rest_framework import serializers
from django.db import transaction

from .models import PlayerTransaction, RoomTransaction, FundTransaction
from users.models import Player
from rooms.models import PlayerRoom
from transactions.enums import PlayerTransactionTypeEnum, RoomTransactionTypeEnum, FundTransactionTypeEnum


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
        elif (
            data['type'] == PlayerTransactionTypeEnum.ADMIN_TO_PLAYER_GAME.value
            and
            data['amount'] > self.context.get('fund').balance
        ):
            raise serializers.ValidationError(f"Amount exceeds fund balance of {self.context.get('fund').balance}$")

        if data['type'] == PlayerTransactionTypeEnum.PLAYER_TO_ADMIN_PROFIT.value:
            data['admin_share'] = self._get_admin_share(data['player'], data['amount'])
            data['player_share'] = self._get_player_share(data['player'], data['amount'])

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
            transaction.on_commit(
                lambda: self._update_fund(self.context.get('fund'), -validated_data['amount'])
            )
        elif validated_data['type'] == PlayerTransactionTypeEnum.PLAYER_TO_ADMIN_DUTY.value:
            transaction.on_commit(
                lambda: self._update_player_balance(validated_data['player'], -validated_data['amount'])
            )
            transaction.on_commit(
                lambda: self._update_player_duty(validated_data['player'], -validated_data['amount'])
            )
            transaction.on_commit(
                lambda: self._update_fund(self.context.get('fund'), validated_data['amount'])
            )
        elif validated_data['type'] == PlayerTransactionTypeEnum.PLAYER_TO_ADMIN_PROFIT.value:
            transaction.on_commit(
                lambda: self._update_player_balance(validated_data['player'], -validated_data['amount'])
            )
            transaction.on_commit(
                lambda: self._update_player_profit(
                    validated_data['player'], validated_data['amount'], self.context.get('fund')
                )
            )
        return player_transaction

    def _get_player_share(self, player, amount):
        return amount * player.rate / 100

    def _get_admin_share(self, player, amount):
        return amount * (100 - player.rate) / 100

    def _update_player_balance(self, player, amount):
        player.balance += amount
        player.save()

    def _update_player_profit(self, player, amount, fund):
        player.current_profit -= amount
        player.admin_profit_share -= self._get_admin_share(player, amount)
        player.self_profit_share -= self._get_player_share(player, amount)
        player.profit_to_admin += self._get_admin_share(player, amount)
        player.salary += self._get_player_share(player, amount)
        player.save()
        fund.balance += amount * (100 - player.rate) / 100
        fund.save()

    def _update_player_duty(self, player, amount):
        player.duty += amount
        player.save()

    def _update_fund(self, fund, amount):
        fund.balance += amount
        fund.save()

    class Meta:
        model = PlayerTransaction
        fields = ['id', 'type', 'amount', 'admin', 'created_at', 'admin_share', 'player_share']


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


class FundTransactionSerializer(serializers.ModelSerializer):
    admin_name = serializers.SerializerMethodField()

    def get_admin_name(self, obj):
        return obj.admin.user.get_full_name()

    def validate(self, data):
        if data['amount'] <= 0:
            raise serializers.ValidationError('Cannot withdraw 0 or less money')
        elif data['type'] not in FundTransactionTypeEnum.values():
            raise serializers.ValidationError('Invalid type of transaction')
        elif (
            data['type'] == FundTransactionTypeEnum.WITHDRAWAL.value
            and
            data['amount'] > data['fund'].balance
        ):
            raise serializers.ValidationError(
                f"Amount exceeds available fund balance {data['fund'].balance}$"
            )
        return data

    @transaction.atomic
    def create(self, validated_data):
        transaction_ = FundTransaction.objects.create(**validated_data)
        if transaction_.type == FundTransactionTypeEnum.WITHDRAWAL.value:
            transaction.on_commit(
                lambda: self._update_fund(validated_data['fund'], -validated_data['amount'])
            )
        elif transaction_.type == FundTransactionTypeEnum.DEPOSIT.value:
            transaction.on_commit(
                lambda: self._update_fund(validated_data['fund'], validated_data['amount'])
            )
        return transaction_

    def _update_fund(self, fund, amount):
        fund.balance += amount
        fund.save()

    class Meta:
        model = FundTransaction
        fields = ['id', 'type', 'amount', 'admin', 'admin_name', 'fund', 'created_at']

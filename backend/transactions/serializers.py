from rest_framework import serializers

from .models import PlayerTransaction, RoomTransaction
from users.models import Player
from transactions.enums import PlayerTransactionEnum


class PlayerTransactionSerializer(serializers.ModelSerializer):
    def validate(self, data):
        if data['amount'] <= 0:
            raise serializers.ValidationError('Нельзя переслать 0 или меньше денег')
        elif not Player.objects.filter(id=data['player_id']).exists():
            raise serializers.ValidationError('Нельзя провести транзакцию с несуществующим пользователем')
        elif data['type'] not in PlayerTransactionEnum:
            raise serializers.ValidationError('Неверный тип транзакции')

    class Meta:
        model = PlayerTransaction
        fields = ['type', 'amount']


class RoomTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomTransaction
        fields = ['type', 'amount']

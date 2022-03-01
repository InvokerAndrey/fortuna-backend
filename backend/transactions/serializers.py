from rest_framework import serializers

from .models import PlayerTransaction, RoomTransaction
from users.models import Player
from rooms.models import PlayerRoom
from transactions.enums import PlayerTransactionEnum, RoomTransactionEnum


class PlayerTransactionSerializer(serializers.ModelSerializer):
    def validate(self, data):
        if data['amount'] <= 0:
            raise serializers.ValidationError('Нельзя переслать 0 или меньше денег')
        elif not Player.objects.filter(id=data['player_id']).exists():
            raise serializers.ValidationError('Нельзя провести транзакцию с несуществующим пользователем')
        elif data['type'] not in PlayerTransactionEnum:
            raise serializers.ValidationError('Неверный тип транзакции')
        return data

    class Meta:
        model = PlayerTransaction
        fields = ['id', 'type', 'amount', 'created_at']


class RoomTransactionSerializer(serializers.ModelSerializer):
    def validate(self, data):
        if data['amount'] <= 0:
            raise serializers.ValidationError('Нельзя переслать 0 или меньше денег')
        elif not PlayerRoom.objects.filter(id=data['room_id']).exists():
            raise serializers.ValidationError('Нельзя провести транзакцию с несуществующим румом')
        elif data['type'] not in RoomTransactionEnum:
            raise serializers.ValidationError('Неверный тип транзакции')
        return data

    class Meta:
        model = RoomTransaction
        fields = ['id', 'type', 'amount', 'created_at']

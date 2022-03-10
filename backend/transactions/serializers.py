from rest_framework import serializers

from .models import PlayerTransaction, RoomTransaction
from users.models import Player
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
        data['admin'] = self.context.get('admin_user').admin
        return data

    def create(self, validated_data):
        return PlayerTransaction.objects.create(**validated_data)

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
            print('Нельзя провести транзакцию с несуществующим румом')
            raise serializers.ValidationError('Нельзя провести транзакцию с несуществующим румом')
        elif data['type'] not in RoomTransactionEnum.values():
            raise serializers.ValidationError('Неверный тип транзакции')
        data['room'] = PlayerRoom.objects.get(id=self.context.get('player_room_id'))
        data['player'] = self.context.get('player')
        return data

    def create(self, validated_data):
        return RoomTransaction.objects.create(**validated_data)

    class Meta:
        model = RoomTransaction
        fields = ['id', 'type', 'amount', 'room_name', 'created_at']

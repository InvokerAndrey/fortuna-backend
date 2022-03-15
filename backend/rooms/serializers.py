from rest_framework import serializers

from .models import Room, PlayerRoom
from users.models import Player


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['id', 'name', 'description', 'website']


class PlayerRoomSerializer(serializers.ModelSerializer):
    info = RoomSerializer(source='room')

    class Meta:
        model = PlayerRoom
        fields = ['id', 'info', 'nickname', 'balance']


class AddPlayerRoomSerializer(serializers.Serializer):
    room_name = serializers.CharField(max_length=100)
    balance = serializers.DecimalField(max_digits=12, decimal_places=2)
    nickname = serializers.CharField(max_length=100)

    def validate(self, data):
        if PlayerRoom.objects.filter(room__name=data['room_name']).exists():
            raise serializers.ValidationError('Такой рум уже есть у игрока')
        elif data['balance'] < 0:
            raise serializers.ValidationError('Баланс не может быть отрицательным')
        elif not Player.objects.filter(pk=self.context.get('player_id')).exists():
            raise serializers.ValidationError('Такого пользователя не существует')

        room = Room.objects.get(name=data['room_name'])
        del data['room_name']
        data['room'] = room
        data['player'] = Player.objects.get(pk=self.context.get('player_id'))
        return data

    def create(self, validated_data):
        return PlayerRoom.objects.create(**validated_data)


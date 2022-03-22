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
        data['player'] = Player.objects.get(pk=self.context.get('player_id'))

        if PlayerRoom.objects.filter(player=data['player'], room__name=data['room_name']).exists():
            raise serializers.ValidationError('The player already has such a room')
        elif data['balance'] < 0:
            raise serializers.ValidationError('Balance cannot be negative')
        elif not Player.objects.filter(pk=self.context.get('player_id')).exists():
            raise serializers.ValidationError('No such user exists')

        room = Room.objects.get(name=data['room_name'])
        del data['room_name']
        data['room'] = room
        return data

    def create(self, validated_data):
        return PlayerRoom.objects.create(**validated_data)


class PlayerRoomStatistics(serializers.ModelSerializer):
    class Meta:
        model = PlayerRoom
        fields = ['id', 'profit', ]

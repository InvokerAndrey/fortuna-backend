from rest_framework import serializers

from .models import Room, PlayerRoom


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['id', 'name', 'description', 'website']


class PlayerRoomSerializer(serializers.ModelSerializer):
    info = RoomSerializer(source='room')

    class Meta:
        model = PlayerRoom
        fields = ['id', 'info', 'nickname', 'balance']

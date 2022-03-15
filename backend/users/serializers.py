from rest_framework import serializers

from .models import Admin, Player, User, Fund
from rooms.serializers import PlayerRoomSerializer
from transactions.serializers import PlayerTransactionSerializer, RoomTransactionSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='get_full_name')

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'full_name', 'email', 'is_staff']


class UserSerializerWithToken(UserSerializer):
    token = serializers.SerializerMethodField()

    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'full_name', 'email', 'is_staff', 'token']


class UserTokenObtainPairSerializer(TokenObtainPairSerializer):
    default_error_messages = {
        'no_active_account': 'Wrong Email or Password'
    }

    def validate(self, attrs):
        data = super().validate(attrs)
        serializer = UserSerializerWithToken(self.user, many=False)
        for k, v in serializer.data.items():
            data[k] = v
        return data


class FundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fund
        fields = ['id', 'balance']


class AdminListSerializer(serializers.ModelSerializer):
    fund = FundSerializer()
    user = UserSerializerWithToken()

    class Meta:
        model = Admin
        fields = ['id', 'rate', 'profit_share', 'fund', 'user']


class PlayerListSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Player
        fields = ['id', 'rate', 'user']


class PlayerDetailsSerializer(serializers.ModelSerializer):
    user = UserSerializerWithToken()
    rooms = serializers.SerializerMethodField()
    player_transactions = serializers.SerializerMethodField()
    room_transactions = serializers.SerializerMethodField()

    def get_rooms(self, obj):
        return PlayerRoomSerializer(obj.playerroom_set.all(), many=True).data

    def get_player_transactions(self, obj):
        return PlayerTransactionSerializer(obj.playertransaction_set.all(), many=True).data

    def get_room_transactions(self, obj):
        return RoomTransactionSerializer(obj.roomtransaction_set.all(), many=True).data

    class Meta:
        model = Player
        fields = ['id', 'user', 'rate', 'rooms', 'player_transactions', 'room_transactions', 'balance']


class PlayerForSessionSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Player
        fields = ['id', 'user', 'rate']

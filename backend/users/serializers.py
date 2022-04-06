from rest_framework import serializers

from .models import Admin, Player, User, Fund
from rooms.serializers import PlayerRoomSerializer
from transactions.serializers import PlayerTransactionSerializer, RoomTransactionSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rooms.models import PlayerRoom
from transactions.enums import PlayerTransactionTypeEnum
from transactions.models import PlayerTransaction


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


class AdminsForFundSerializer(serializers.ModelSerializer):
    user = UserSerializerWithToken()

    class Meta:
        model = Admin
        fields = ['id', 'user', 'rate', 'profit_share']


class FundSerializer(serializers.ModelSerializer):
    admins = serializers.SerializerMethodField()
    in_game = serializers.SerializerMethodField()
    profit = serializers.SerializerMethodField()

    def get_admins(self, obj):
        return AdminsForFundSerializer(obj.admin_set.all(), many=True).data

    def get_in_game(self, obj):
        return sum([player.duty for player in Player.objects.all()])

    def get_profit(self, obj):
        return sum([player.profit_to_admin for player in Player.objects.all()])

    class Meta:
        model = Fund
        fields = ['id', 'balance', 'admins', 'in_game', 'profit']


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
    total_rooms_balance = serializers.SerializerMethodField()

    def get_rooms(self, obj):
        return PlayerRoomSerializer(obj.playerroom_set.all(), many=True).data

    def get_player_transactions(self, obj):
        return PlayerTransactionSerializer(obj.playertransaction_set.all(), many=True).data

    def get_room_transactions(self, obj):
        return RoomTransactionSerializer(obj.roomtransaction_set.all(), many=True).data

    def get_total_rooms_balance(self, obj):
        player_rooms = PlayerRoom.objects.filter(player=obj)
        return sum([room.balance for room in player_rooms])

    class Meta:
        model = Player
        fields = [
            'id',
            'user',
            'rate',
            'rooms',
            'player_transactions',
            'room_transactions',
            'balance',
            'total_rooms_balance',
            'duty',
            'all_time_profit',
            'salary',
            'admin_profit_share',
            'self_profit_share',
            'current_profit',
            'profit_to_admin',
        ]


class PlayerForSessionSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Player
        fields = ['id', 'user', 'rate']

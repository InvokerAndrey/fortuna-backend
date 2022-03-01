from rest_framework_simplejwt.views import TokenObtainPairView

from .models import Admin, Player
from .serializers import (
    AdminListSerializer,
    PlayerListSerializer,
    UserTokenObtainPairSerializer,
    PlayerDetailsSerializer,
)
from core.views import BaseListView, BaseDetailView


class UserTokenObtainPairView(TokenObtainPairView):
    serializer_class = UserTokenObtainPairSerializer


class AdminListView(BaseListView):
    model = Admin
    serializer_class = AdminListSerializer
    related_fields = ['user', 'fund']


class PlayerListView(BaseListView):
    model = Player
    serializer_class = PlayerListSerializer
    related_fields = ['user']


class PlayerDetailView(BaseDetailView):
    model = Player
    serializer_class = PlayerDetailsSerializer

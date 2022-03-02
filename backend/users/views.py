from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework.response import Response
from rest_framework import status
from django.db.utils import IntegrityError

from .models import Admin, Player, Fund
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
    permission_classes = [IsAdminUser]


class PlayerListView(BaseListView):
    model = Player
    serializer_class = PlayerListSerializer
    related_fields = ['user']
    permission_classes = [IsAdminUser]


class PlayerDetailView(BaseDetailView):
    model = Player
    serializer_class = PlayerDetailsSerializer
    permission_classes = [IsAdminUser]


@api_view(['POST'])
@permission_classes([IsAdminUser])
def register_player(request):
    data = request.data
    try:
        user = User.objects.create(
            email=data['email'],
            username=data['username'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            is_staff=False,
            password=make_password(data['password']),
        )
        user.save()
        player = Player.objects.create(
            user=user,
            rate=data['rate'],
        )
        serializer = PlayerDetailsSerializer(player, many=False)
        return Response(serializer.data)
    except IntegrityError:
        message = {'details': 'Такой пользователь уже существует'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAdminUser])
def register_admin(request):
    data = request.data
    try:
        user = User.objects.create(
            email=data['email'],
            username=data['username'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            is_staff=True,
            password=make_password(data['password']),
        )
        fund = Fund.objects.first()
        admin = Admin.objects.create(
            user=user,
            fund=data.get('fund') or fund,
            rate=data['rate'],
        )
        serializer = AdminListSerializer(admin, many=False)
        return Response(serializer.data)
    except IntegrityError:
        message = {'details': 'Такой пользователь уже существует'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)

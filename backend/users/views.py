from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
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
    order_by = ['user__last_name']


class PlayerListView(BaseListView):
    model = Player
    serializer_class = PlayerListSerializer
    related_fields = ['user']
    permission_classes = [IsAdminUser]
    order_by = ['user__last_name']


class PlayerDetailView(BaseDetailView):
    model = Player
    serializer_class = PlayerDetailsSerializer
    permission_classes = [IsAdminUser]


@api_view(['POST'])
@permission_classes([IsAdminUser])
def register_player(request):
    data = request.data
    if float(data['rate']) < 0 or float(data['rate']) > 100:
        return Response({'detail': 'Rate must be in 0-100 range'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        user = User.objects.create(
            email=data['email'],
            username=data['email'],
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
        message = {'detail': 'This user already exists'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAdminUser])
def register_admin(request):
    data = request.data
    if float(data['rate']) < 0 or float(data['rate']) > 100:
        return Response({'detail': 'Rate must be in 0-100 range'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        if not data.get('fund'):
            return Response({'detail': 'There is no any fund'}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.create(
            email=data['email'],
            username=data['email'],
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
        message = {'detail': 'This user already exists'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def delete_player(request, pk):
    player = get_object_or_404(Player, pk=pk)
    player.user.delete()
    return Response(status=status.HTTP_202_ACCEPTED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_player_profile(request, pk):
    player = User.objects.get(pk=pk).player
    serializer = PlayerDetailsSerializer(player, many=False)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAdminUser])
def update_player_info(request, pk):
    data = request.data
    player = Player.objects.get(pk=pk)
    user = player.user
    user.email = data['email']
    user.first_name = data['first_name']
    user.last_name = data['last_name']
    player.rate = data['rate']
    user.save()
    player.save()
    serializer = PlayerDetailsSerializer(player, many=False)
    return Response(serializer.data)

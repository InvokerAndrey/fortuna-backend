from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser

from users.models import Admin
from .models import PlayerTransaction
from .serializers import PlayerTransactionSerializer


class CreatePlayerTransaction(APIView):
    def post(self, request):
        admin = request.user.admin
        serializer = PlayerTransactionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAdminUser])
def add_player_transaction(request, pk):
    pass

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

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

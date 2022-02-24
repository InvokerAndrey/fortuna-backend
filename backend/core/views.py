from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response


class BaseListView(APIView):
    model = None
    serializer_class = None
    related_fields = []

    def get(self, request):
        obj_qs = self.model.objects.select_related(*self.related_fields)
        serializer = self.serializer_class(obj_qs, many=True)
        return Response(serializer.data)


class BaseDetailView(APIView):
    model = None
    serializer_class = None

    def get_obj(self, pk):
        return get_object_or_404(self.model, pk=pk)

    def get(self, request, pk):
        obj = self.get_obj(pk)
        serializer = self.serializer_class(obj, many=False)
        return Response(serializer.data)

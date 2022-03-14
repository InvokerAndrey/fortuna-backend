from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination


class Pagination(PageNumberPagination):
    def get_paginated_response(self, data):
        return Response(dict([
            ('page', self.page.number),
            ('count', self.page.paginator.count),
            ('num_pages', self.page.paginator.num_pages),
            ('results', data),
        ]))


class BaseListView(APIView):
    model = None
    serializer_class = None
    related_fields = []

    def get(self, request):
        paginator = Pagination()
        obj_qs = self.model.objects.select_related(*self.related_fields)
        page = paginator.paginate_queryset(obj_qs, request)
        serializer = self.serializer_class(page, many=True)
        return paginator.get_paginated_response(serializer.data)


class BaseDetailView(APIView):
    model = None
    serializer_class = None

    def get_obj(self, pk):
        return get_object_or_404(self.model, pk=pk)

    def get(self, request, pk):
        obj = self.get_obj(pk)
        serializer = self.serializer_class(obj, many=False)
        return Response(serializer.data)

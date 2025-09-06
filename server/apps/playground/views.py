# from django.shortcuts import render
from django.http import Http404
from rest_framework.decorators import api_view
from rest_framework.generics import (
    GenericAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.mixins import (
    CreateModelMixin,  # 負責處理建立 (POST)
    DestroyModelMixin,  # 負責處理刪除 (DELETE)
    ListModelMixin,  # 負責列表 (GET)
    RetrieveModelMixin,  # 負責單一物件存取 (GET)
    UpdateModelMixin,  # 負責更新 (PUT, PATCH)
)
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from server.apps.management.serializer import ItemSerializer
from server.apps.playground.models import Item
from server.utils import PageNumberSizePagination

# Create your views here.


@api_view(["GET", "POST"])
def hello(request):
    if request.method == "POST":
        message = "Hello, POST request received!"
    else:
        message = "Hello, GET request received!"

    return Response({"message": message})


class HiView(APIView):
    def _build_message(self, method):
        return f"Hello, {method} request received!"

    def get(self, request):
        message = self._build_message("GET")
        return Response({"message": message})

    def post(self, request):
        return Response({"message": self._build_message("POST")})


class ItemView(APIView):
    def get(self, request):
        items = Item.objects.all()
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data)

    def post(self, request):
        # item_data = request.data
        # validate request data
        serializer = ItemSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        # Item.objects.create(**serializer.validated_data)
        Item.objects.create(**serializer.validated_data)
        # Here you would typically save the item to the database
        return Response(
            {"message": "Item created", "Record instert": serializer.data}, status=201
        )


# GET /xxxxxx/items/<id> => 得到資料庫中指定的 Items
# GET /xxxxxx/items => 得到資料庫中所有的 Items


class ItemListView(ListCreateAPIView):
    serializer_class = ItemSerializer
    queryset = Item.objects.all()


# GET /xxxxxx/items/<id> => 得到資料庫中指定的 Items

## 版本一
# class ItemDetailView(
#     RetrieveModelMixin, DestroyModelMixin, UpdateModelMixin, GenericAPIView
# ):
#     serializer_class = ItemSerializer
#     queryset = Item.objects.all()
#     lookup_url_kwarg = "item_id"

#     def get(self, request, item_id):
#         return self.retrieve(request, item_id)

#     def delete(self, request, item_id):
#         return self.destroy(request, item_id)

#     def put(self, request, item_id):
#         return self.update(request, item_id)

#     def patch(self, request, item_id):
#         return self.partial_update(request, item_id)


## 版本二
class ItemDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = ItemSerializer
    queryset = Item.objects.all()
    lookup_url_kwarg = "item_id"


## ViewSet
class ItemViewSet(ModelViewSet):
    serializer_class = ItemSerializer
    queryset = Item.objects.order_by("id")
    pagination_class = PageNumberSizePagination


# class ItemDetailView(GenericAPIView):
#     serializer_class = ItemSerializer
#     queryset = Item.objects.all()
#     lookup_url_kwarg = "item_id"

# def get(self, request, item_id):
#     item = self.get_object()
#     serializer = self.get_serializer(item)
#     return Response(serializer.data)

# def delete(self, request, item_id):
#     item = self.get_object()
#     item.delete()
#     return Response({"message": "Item deleted"}, status=204)

# def put(self, request, item_id):
#     item = self.get_object()
#     serializer = self.get_serializer(item, data=request.data)
#     if not serializer.is_valid():
#         return Response(serializer.errors, status=400)
#     serializer.save()
#     return Response(serializer.data)

# def patch(self, request, item_id):
#     item = self.get_object()
#     serializer = self.get_serializer(item, data=request.data, partial=True)
#     if not serializer.is_valid():
#         return Response(serializer.errors, status=400)
#     serializer.save()
#     return Response(serializer.data)

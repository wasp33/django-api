# from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.generics import GenericAPIView, ListCreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from server.apps.management.serializer import ItemSerializer
from server.apps.playground.models import Item

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


class ItemDetailView(GenericAPIView):
    serializer_class = ItemSerializer

    def get_item(self, item_id):
        try:
            return Item.objects.get(id=item_id)
        except Item.DoesNotExist:
            return Response({"error": "Item not found"}, status=404)

    def get(self, request, item_id):
        item = self.get_item(item_id)
        serializer = self.get_serializer(item)
        return Response(serializer.data)

    def delete(self, request, item_id):
        item = self.get_item(item_id)
        item.delete()
        return Response({"message": "Item deleted"}, status=204)

    def put(self, request, item_id):
        item = self.get_item(item_id)
        serializer = self.get_serializer(item, data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)
        serializer.save()
        return Response(serializer.data)

    def patch(self, request, item_id):
        item = self.get_item(item_id)
        serializer = self.get_serializer(item, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)
        serializer.save()
        return Response(serializer.data)

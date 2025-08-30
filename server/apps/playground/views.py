# from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

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

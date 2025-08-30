from django.urls import path

from server.apps.playground.views import HiView, ItemDetailView, ItemView, hello

urlpatterns = [
    path("hello", hello),
    path("hi", HiView.as_view()),
    path("items", ItemView.as_view()),
    path("items/<int:item_id>/", ItemDetailView.as_view()),
]

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from server.apps.playground.views import (
    HiView,
    ItemDetailView,
    ItemView,
    ItemViewSet,
    hello,
)

router = DefaultRouter(trailing_slash=False)
router.register(r"items-v2", ItemViewSet, basename="item")

urlpatterns = [
    path("hello", hello),
    path("hi", HiView.as_view()),
    path("items", ItemView.as_view()),
    path("items/<int:item_id>/", ItemDetailView.as_view()),
    path("viewset/", include(router.urls)),
]

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from inventory.views.book import BookViewSet

router = DefaultRouter()
router.register(r'books', BookViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
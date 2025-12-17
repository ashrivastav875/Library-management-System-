"""
Ratings app URL configuration.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookRatingViewSet

router = DefaultRouter()
router.register(r'ratings', BookRatingViewSet, basename='rating')

urlpatterns = [
    path('', include(router.urls)),
]

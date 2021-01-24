from django.urls import path, include
from rest_framework import routers
from .api import CommentViewSet

app_name = 'data'

router = routers.DefaultRouter()

router.register(r"comments/(?P<post>\d+)", CommentViewSet, basename="comment")

urlpatterns = router.urls


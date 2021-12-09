from .views import ImageViewSet, get_status, analyze_image
from rest_framework import routers
from django.urls import path, include

router = routers.DefaultRouter()
# router.register(r'analyze_im', ImageViewSet)

urlpatterns = [
    path('analyze_im/', analyze_image, name="analyze_image"),
    path('task/<task_id>/', get_status, name="get_status"),

]

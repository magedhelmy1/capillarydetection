from django.urls import path
from rest_framework import routers

from .views import analyze_image, get_status

# router = routers.DefaultRouter()
# router.register(r'analyze_im', ImageViewSet)

urlpatterns = [
    path('analyze_im/', analyze_image, name="analyze_image"),
    path('task/<task_id>/', get_status, name="get_status"),
]

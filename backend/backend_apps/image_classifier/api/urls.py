from .views import ImageViewSet, get_status, analyze_image, test_Response, test_RPSs
from rest_framework import routers
from django.urls import path, include

router = routers.DefaultRouter()
# router.register(r'analyze_im', ImageViewSet)

urlpatterns = [
    path('analyze_im/', test_RPSs, name="analyze_image"),
    path('task/<task_id>/', test_Response, name="get_status"),

]



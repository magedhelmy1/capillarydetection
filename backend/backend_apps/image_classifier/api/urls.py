from django.urls import path
from rest_framework import routers

from .views import get_status  # , process_image

router = routers.DefaultRouter()
# router.register(r'analyze_im', ImageViewSet)

urlpatterns = [
    # path('', include(router.urls)),
    # path('analyze_im/', process_image, name="process_image"),
    path('task/<task_id>/', get_status, name="get_status"),
]

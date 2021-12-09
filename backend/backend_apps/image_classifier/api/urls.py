from .views import ImageViewSet, get_status,process_image
from rest_framework import routers
from django.urls import path, include

router = routers.DefaultRouter()
router.register(r'analyze_im', ImageViewSet)

urlpatterns = [
    # path('', include(router.urls)),
    path('analyze_im/', process_image, name="process_image"),
    path('task/<task_id>/', get_status, name="get_status"),

]

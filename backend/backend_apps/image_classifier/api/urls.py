from .views import ImageViewSet, get_status #, create
from rest_framework import routers
from django.urls import path, include

router = routers.DefaultRouter()
router.register(r'analyze_im', ImageViewSet)

urlpatterns = [
    path('', include(router.urls)),
    #path('analyze_im/', create, name="create"),
    path('task/<task_id>/', get_status, name="get_status"),

]

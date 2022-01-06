"""server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from image_classifier.views import hello, performance_test, async_image_analyze, get_status

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include('image_classifier.api.urls')),
    path('api/hello/', hello, name='hello'),
    path('api/performance_test/', performance_test, name='performance_test'),
    path('api/async_image_analyze/', async_image_analyze, name='async_image_analyze'),
    path('task/<task_id>/', get_status, name="get_status"),
]

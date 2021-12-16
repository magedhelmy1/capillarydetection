from asgiref.sync import sync_to_async
from rest_framework import viewsets
from .serializers import ImageSerializer
from ..models import Image
from rest_framework.response import Response
from celery import shared_task, current_app
import os
from django.conf import settings
from rest_framework import status
from ..tasks import algorithm_image
from django.http import JsonResponse
from rest_framework.decorators import api_view
import time


class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer



@api_view(('GET',))
def get_status(request, task_id):
    task = current_app.AsyncResult(task_id)
    context = {'task_status': task.status, 'task_id': task.id}

    if task.status == 'PENDING':
        return Response({**context}, status=status.HTTP_200_OK)
    else:
        response_data = task.get()
        return Response({**context, **response_data}, status=status.HTTP_201_CREATED)

from celery import current_app
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import ImageSerializer
from ..models import Image


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

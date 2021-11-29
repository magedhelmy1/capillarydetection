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

    def create(self, request, *args, **kwargs):
        serializer = ImageSerializer(data=request.data)

        test = False
        if serializer.is_valid() and test:
            image_name = "test.png"
            result = algorithm_image.delay("test", image_name, True)

            return JsonResponse({"task_id": result.id,
                                 "task_status": result.status},
                                status=status.HTTP_200_OK)

        elif serializer.is_valid() and not test:

            image_uploaded = serializer.validated_data['picture']
            image_name = str(serializer.validated_data['picture'])
            file_path = os.path.join(settings.IMAGES_DIR, image_name, )

            with open(file_path, 'wb+') as fp:
                for chunk in image_uploaded:
                    fp.write(chunk)

            result = algorithm_image.delay(file_path, image_name, test=False)

            return JsonResponse({"task_id": result.id,
                                 "task_status": result.status},
                                status=status.HTTP_200_OK)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(('GET',))
def get_status(request, task_id):
    task = current_app.AsyncResult(task_id)
    context = {'task_status': task.status, 'task_id': task.id}

    if task.status == 'PENDING':
        time.sleep(1)
        return Response({**context}, status=status.HTTP_200_OK)
    else:
        response_data = ImageSerializer(Image.objects.get(pk=task.get()))
        return Response({**context, **response_data.data}, status=status.HTTP_201_CREATED)

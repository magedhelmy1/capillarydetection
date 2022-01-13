import os

from celery import current_app
from django.conf import settings
from django.http import JsonResponse
from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import ImageSerializer
from ..models import Image
from ..tasks import algorithm_image


class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer


@api_view(('POST',))
def analyze_image(request, **kwargs):
    serializer = ImageSerializer(data=request.data)

    test = False
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif serializer.is_valid() and test:
        image_name = "test.png"

        # result = algorithm_image("test", image_name, True)
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

        # result = algorithm_image(file_path, image_name, False)
        result = algorithm_image.delay(file_path, image_name, False)
        print(result)

        return JsonResponse({"task_id": result.id,
                             "task_status": result.status},
                            status=status.HTTP_200_OK)


@api_view(('GET',))
def get_status(request, task_id):
    task = current_app.AsyncResult(task_id)
    context = {'task_status': task.status, 'task_id': task.id}

    if task.status == 'PENDING':
        return Response({**context}, status=status.HTTP_200_OK)

    else:
        response_data = task.get()
        print(f"Response data is {response_data}")

        return Response({**context, **response_data}, status=status.HTTP_201_CREATED)

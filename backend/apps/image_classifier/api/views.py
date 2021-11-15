from rest_framework import viewsets
from .serializers import ImageSerializer
from ..models import Image
from rest_framework.decorators import api_view
from ..classifier_script import classify_image
import traceback
from io import BytesIO
from rest_framework.response import Response
from rest_framework import status
from django.core.files import File
from celery import shared_task
import json, numpy as np
import base64
import json
import pickle


class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all().order_by('-uploaded')
    serializer_class = ImageSerializer

    def create(self, request, *args, **kwargs):
        serializer = ImageSerializer(data=request.data)

        if serializer.is_valid():
            image_uploaded = "mediafiles/sample_images/1.png"
            json_data = base64.b64encode(np.array(image_uploaded)).decode('ascii')
            result = algorithm_image.delay(json_data)
            result_unpacked = ImageSerializer(Image.objects.get(pk=result.get()))

            return Response(result_unpacked.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@shared_task(name="values")
def algorithm_image(serializer):
    file_name = str(serializer)
    pictures = serializer

    time_taken, analyzed, number_capillaries, area_of_capillaries, segmented_image_clean = \
        classify_image(pictures)

    new_image_io = BytesIO()
    analyzed.save(new_image_io, format='PNG')
    analyzed_file_object = File(new_image_io, name=file_name)

    new_image_io_segmented = BytesIO()
    segmented_image_clean.save(new_image_io_segmented, format='PNG')
    segmented_file_object = File(new_image_io_segmented, name=file_name)

    model_instance = Image.objects.create()
    model_instance.picture = pictures
    model_instance.time_to_classify = time_taken
    model_instance.number_of_capillaries = number_capillaries
    model_instance.capillary_area = area_of_capillaries
    model_instance.analyzed_picture = analyzed_file_object
    model_instance.segmented_image = segmented_file_object
    model_instance.save()

    return model_instance.id

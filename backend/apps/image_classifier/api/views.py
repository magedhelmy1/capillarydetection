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


class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all().order_by('-uploaded')
    serializer_class = ImageSerializer

    @shared_task(name="get values")
    def create(self, request, *args, **kwargs):

        serializer = ImageSerializer(data=self.request.POST)

        if serializer.is_valid() and serializer.validated_data['backend_address'] is not None:
            image_uploaded = "mediafiles/sample_images/1.png"
            file_name = str(image_uploaded)


        else:
            image_uploaded = serializer.validated_data['picture']
            file_name = str(image_uploaded)

        try:
            time_taken, analyzed, number_capillaries, area_of_capillaries, segmented_image_clean = \
                classify_image(image_uploaded)

            new_image_io = BytesIO()
            analyzed.save(new_image_io, format='PNG')
            analyzed_file_object = File(new_image_io, name=file_name)

            new_image_io_segmented = BytesIO()
            segmented_image_clean.save(new_image_io_segmented, format='PNG')
            segmented_file_object = File(new_image_io_segmented, name=file_name)

            serializer.save(time_to_classify=time_taken,
                            number_of_capillaries=number_capillaries,
                            capillary_area=area_of_capillaries,
                            analyzed_picture=analyzed_file_object,
                            segmented_image=segmented_file_object)

            print("Classification success")

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:

            print("classification failed: ", traceback.format_exc())
            return Response(e.args[0], status.HTTP_400_BAD_REQUEST)

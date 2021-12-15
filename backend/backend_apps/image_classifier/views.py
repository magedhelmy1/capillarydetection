from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view

from .tasks import algorithm_image
from django.http import JsonResponse
from django.shortcuts import render
import json
from django.views.decorators.csrf import csrf_protect
import os
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile


# Experimenting with ASGI

async def hello(request):
    return HttpResponse("Hello, async Django!")


async def performance_test(request):
    res = await performance_test_process_image(request)

    json_data = json.loads(res.content)

    return render(request, "index.html", {"task_id": json_data["task_id"],
                                          "task_status": json_data["task_status"]})


async def performance_test_process_image(request, *args, **kwargs):
    image_name = "test.png"

    result = algorithm_image.delay("test", image_name, True)

    return JsonResponse({"task_id": result.id,
                         "task_status": result.status},
                        status=status.HTTP_200_OK)


async def async_image_analyze(request):
    if request.method == 'POST':
        result = await image_algorithm(request)
        json_data = json.loads(result.content)

        return JsonResponse({"task_id": json_data["task_id"],
                             "task_status": json_data["task_status"]},
                            status=status.HTTP_200_OK)


async def image_algorithm(request, *args, **kwargs):
    if request.method == 'POST':
        image_name = str(request.FILES["picture"])
        file_path = os.path.join(settings.IMAGES_DIR, image_name)
        path = default_storage.save(file_path, ContentFile(request.FILES["picture"].read()))

        # with open(file_path, 'wb+') as fp:
        #     for chunk in image_uploaded:
        #         fp.write(chunk)

        result = algorithm_image.apply_async((path, image_name, False), queue='transient')

        return JsonResponse({"task_id": result.id,
                             "task_status": result.status},
                            status=status.HTTP_200_OK)

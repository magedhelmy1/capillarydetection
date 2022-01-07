import asyncio
import json
import os

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status

from .tasks import algorithm_image


# Base test
async def hello(request):
    return HttpResponse("Hello, async Django!")


# Test Step
@csrf_exempt
async def performance_test(request):
    task1 = asyncio.create_task(performance_test_process_image())
    res = await task1

    # res = await performance_test_process_image()
    json_data = json.loads(res.content)

    return render(request, "index.html", {"task_id": json_data["task_id"],
                                          "task_status": json_data["task_status"]})


@csrf_exempt
async def performance_test_process_image():
    image_name = "test.png"

    result = algorithm_image.delay("test", image_name, True)

    return JsonResponse({"task_id": result.id,
                         "task_status": result.status},
                        status=status.HTTP_200_OK)


# Live Step
@csrf_exempt
async def async_image_analyze(request):
    task1 = asyncio.create_task(image_algorithm(request))
    res = await task1
    json_data = json.loads(res.content)

    return JsonResponse({"task_id": json_data["task_id"],
                         "task_status": json_data["task_status"]},
                        status=status.HTTP_200_OK)


@csrf_exempt
async def image_algorithm(request, *args, **kwargs):
    image_name = str(request.FILES["picture"])
    file_path = os.path.join(settings.IMAGES_DIR, image_name)
    path = default_storage.save(file_path, ContentFile(request.FILES["picture"].read()))
    result = algorithm_image.delay(path, image_name, False)  # , queue='transient')

    return JsonResponse({"task_id": result.id,
                         "task_status": result.status},
                        status=status.HTTP_200_OK)

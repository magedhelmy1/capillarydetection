import json
import os

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from rest_framework import status

from .tasks import algorithm_image


#Base test
async def hello(request):
    return HttpResponse("Hello, async Django!")


async def performance_test(request):
    res = await performance_test_process_image()
    json_data = json.loads(res.content)

    return render(request, "index.html", {"task_id": json_data["task_id"],
                                          "task_status": json_data["task_status"]})


async def performance_test_process_image():
    image_name = "test.png"

    result = algorithm_image.delay("test", image_name, True)
    # result = algorithm_image.apply_async(("test", image_name, True), queue='transient')

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
    image_name = str(request.FILES["picture"])
    file_path = os.path.join(settings.IMAGES_DIR, image_name)
    path = default_storage.save(file_path, ContentFile(request.FILES["picture"].read()))
    result = algorithm_image.delay(path, image_name, False)  # , queue='transient')

    return JsonResponse({"task_id": result.id,
                         "task_status": result.status},
                        status=status.HTTP_200_OK)

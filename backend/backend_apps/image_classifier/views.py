from django.http import HttpResponse
from rest_framework import status
from .tasks import algorithm_image
from django.http import JsonResponse
from django.shortcuts import render
import json

# Experimenting with ASGI

async def hello(request):
    return HttpResponse("Hello, async Django!")


async def example(request):
    res = await process_image(request)

    json_data = json.loads(res.content)

    return render(request, "index.html", {"task_id": json_data["task_id"],
                                          "task_status": json_data["task_status"]})


async def process_image(request, *args, **kwargs):
    image_name = "test.png"

    result = algorithm_image.delay("test", image_name, True)

    return JsonResponse({"task_id": result.id,
                         "task_status": result.status},
                        status=status.HTTP_200_OK)

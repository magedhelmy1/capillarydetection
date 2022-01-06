import asyncio
import os

from asgiref.sync import sync_to_async
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.http import HttpResponse, JsonResponse
from rest_framework import status

from .tasks import algorithm_image


# Base test
async def hello(request):
    return HttpResponse("Hello, async Django!")


async def performance_test(request):
    task1 = asyncio.create_task(performance_test_process_image())
    res = await task1

    return JsonResponse({"picture": res["picture"],
                         "time_to_classify": res["time_to_classify"],
                         "number_of_capillaries": res["number_of_capillaries"],
                         "capillary_area": res["capillary_area"],
                         "analyzed_picture": res["analyzed_picture"],
                         "segmented_image": res["segmented_image"],
                         },
                        status=status.HTTP_200_OK)

    # res = await performance_test_process_image()
    # json_data = json.loads(res.content)
    # return render(request, "index.html", {"task_id": json_data["task_id"],
    #                                       "task_status": json_data["task_status"]})


@sync_to_async
def performance_test_process_image():
    image_name = "test.png"

    result = algorithm_image("test", image_name, True)

    # result = algorithm_image.apply_async(("test", image_name, True), queue='transient')

    return result


async def async_image_analyze(request):
    if request.method == 'POST':
        task1 = asyncio.create_task(image_algorithm(request))
        res = await task1

        return JsonResponse({"picture": res["picture"],
                             "time_to_classify": res["time_to_classify"],
                             "number_of_capillaries": res["number_of_capillaries"],
                             "capillary_area": res["capillary_area"],
                             "analyzed_picture": res["analyzed_picture"],
                             "segmented_image": res["segmented_image"],
                             },
                            status=status.HTTP_200_OK)


@sync_to_async
def image_algorithm(request, *args, **kwargs):
    image_name = str(request.FILES["picture"])
    file_path = os.path.join(settings.IMAGES_DIR, image_name)
    path = default_storage.save(file_path, ContentFile(request.FILES["picture"].read()))
    # result = algorithm_image.delay(path, image_name, False)  # , queue='transient')
    result = algorithm_image(path, image_name, False)  # , queue='transient')
    return result

    # return JsonResponse({"task_id": result.id,
    #                      "task_status": result.status},
    #                     status=status.HTTP_200_OK)

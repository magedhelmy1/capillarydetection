from django.shortcuts import render
from django.core.files.storage import default_storage
from django.conf import settings
import tensorflow as tf


def index(request):
    if request.method == "POST":
        file = request.FILES["sentFile"]
        response = {}
        file_name = default_storage.save(file.name, file)
        file_url = default_storage.path(file_name)

        img = tf.keras.preprocessing.image.load_img(
            file_url, target_size=(224, 224)
        )

        numpy_image = tf.keras.preprocessing.image.img_to_array(img)
        image_batch = tf.expand_dims(numpy_image, 0)
        predictions = settings.VGG_MODEL.predict(image_batch)
        label = tf.keras.applications.imagenet_utils.decode_predictions(predictions, top=1)
        response['name'] = str(label)

        return render(request, 'homepage.html', response)
    else:
        return render(request, 'homepage.html')


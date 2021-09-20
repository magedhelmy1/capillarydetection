from django.shortcuts import render
from django.core.files.storage import default_storage
from django.conf import settings
import tensorflow as tf


def index(request):
    if request.method == "POST":
        f = request.FILES['sentFile']  # here you get the files needed
        response = {}
        file_name = "pic.jpg"
        file_name_2 = default_storage.save(file_name, f)
        file_url = default_storage.url(file_name_2)

        img = tf.keras.preprocessing.image.load_img(
            file_url, target_size=(224, 224)
        )

        numpy_image = tf.keras.preprocessing.image.img_to_array(img)
        image_batch = tf.expand_dims(numpy_image, 0)
        predictions = settings.VGG_MODEL.predict(image_batch)

        label = list(predictions)[0]
        response['name'] = str(label)
        return render(request, 'homepage.html', response)
    else:
        return render(request, 'homepage.html')

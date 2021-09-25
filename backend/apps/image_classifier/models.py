from django.db import models
from .classifier_script import classify_image
import traceback
from django.core.files.base import ContentFile
from io import BytesIO


# Create your models here.
class Image(models.Model):
    picture = models.ImageField(upload_to="microcirculation_images", blank=True)
    backend_address = models.IntegerField(blank=True, null=True)
    classified = models.CharField(max_length=200, blank=True)
    uploaded = models.DateTimeField(auto_now_add=True)
    analyzed_picture = models.ImageField(upload_to="analyzed_picture", blank=True)
    capillary_density = models.CharField(max_length=200, blank=True)
    number_of_capillaries = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"Image classfied at {self.uploaded.strftime('%Y-%m-%d %H:%M')}"

    def save(self, *args, **kwargs):

        if self.backend_address != None:

            if self.backend_address == 1:
                self.picture = "sample_images/1.png"
                temp_name = "1.png"

            elif self.backend_address == 2:
                self.picture = "sample_images/2.png"
                temp_name = "2.png"

            elif self.backend_address == 3:
                self.picture = "sample_images/3.png"
                temp_name = "3.png"

            else:
                print(f"No Valid Backend Address Detected: {self.backend_address}")

        else:
            temp_name = self.picture.name

        try:

            time_taken, analyzed = classify_image(self.picture)
            self.classified = time_taken

            new_image_io = BytesIO()
            analyzed.save(new_image_io, format='JPEG')

            self.analyzed_picture.save(
                temp_name,
                content=ContentFile(new_image_io.getvalue()),
                save=False
            )

            print(f'success: {self.classified}')

        except Exception as e:
            print("classification failed: ", traceback.format_exc())

        super(Image, self).save(*args, **kwargs)

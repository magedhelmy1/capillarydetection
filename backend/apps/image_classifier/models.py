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
    segmented_image = models.ImageField(upload_to="segmented_image", blank=True)
    capillary_area = models.CharField(max_length=200, blank=True)
    number_of_capillaries = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"Image classfied at {self.uploaded.strftime('%Y-%m-%d %H:%M')}"

    def save(self, *args, **kwargs):

        if self.backend_address != None:

            if self.backend_address == 1:
                self.picture = f"sample_images/{str(self.backend_address)}.png"
                temp_name = f"{str(self.backend_address)}.png"

            elif self.backend_address == 2:
                self.picture = f"sample_images/{str(self.backend_address)}.png"
                temp_name = f"{str(self.backend_address)}.png"

            elif self.backend_address == 3:
                self.picture = f"sample_images/{str(self.backend_address)}.png"
                temp_name = f"{str(self.backend_address)}.png"

            elif self.backend_address == 4:
                self.picture = f"sample_images/{str(self.backend_address)}.png"
                temp_name = f"{str(self.backend_address)}.png"

            elif self.backend_address == 5:
                self.picture = f"sample_images/{str(self.backend_address)}.png"
                temp_name = f"{str(self.backend_address)}.png"

            elif self.backend_address == 6:
                self.picture = f"sample_images/{str(self.backend_address)}.png"
                temp_name = f"{str(self.backend_address)}.png"

            elif self.backend_address == 7:
                self.picture = f"sample_images/{str(self.backend_address)}.png"
                temp_name = f"{str(self.backend_address)}.png"

            elif self.backend_address == 8:
                self.picture = f"sample_images/{str(self.backend_address)}.png"
                temp_name = f"{str(self.backend_address)}.png"

            elif self.backend_address == 9:
                self.picture = f"sample_images/{str(self.backend_address)}.png"
                temp_name = f"{str(self.backend_address)}.png"

            elif self.backend_address == 10:
                self.picture = f"sample_images/{str(self.backend_address)}.png"
                temp_name = f"{str(self.backend_address)}.png"

            elif self.backend_address == 11:
                self.picture = f"sample_images/{str(self.backend_address)}.png"
                temp_name = f"{str(self.backend_address)}.png"

            elif self.backend_address == 12:
                self.picture = f"sample_images/{str(self.backend_address)}.png"
                temp_name = f"{str(self.backend_address)}.png"

            elif self.backend_address == 13:
                self.picture = f"sample_images/{str(self.backend_address)}.png"
                temp_name = f"{str(self.backend_address)}.png"

            elif self.backend_address == 14:
                self.picture = f"sample_images/{str(self.backend_address)}.png"
                temp_name = f"{str(self.backend_address)}.png"

            elif self.backend_address == 15:
                self.picture = f"sample_images/{str(self.backend_address)}.png"
                temp_name = f"{str(self.backend_address)}.png"

            elif self.backend_address == 16:
                self.picture = f"sample_images/{str(self.backend_address)}.png"
                temp_name = f"{str(self.backend_address)}.png"

            elif self.backend_address == 17:
                self.picture = f"sample_images/{str(self.backend_address)}.png"
                temp_name = f"{str(self.backend_address)}.png"

            elif self.backend_address == 18:
                self.picture = f"sample_images/{str(self.backend_address)}.png"
                temp_name = f"{str(self.backend_address)}.png"

            elif self.backend_address == 19:
                self.picture = f"sample_images/{str(self.backend_address)}.png"
                temp_name = f"{str(self.backend_address)}.png"

            elif self.backend_address == 20:
                self.picture = f"sample_images/{str(self.backend_address)}.png"
                temp_name = f"{str(self.backend_address)}.png"

            elif self.backend_address == 21:
                self.picture = f"sample_images/{str(self.backend_address)}.png"
                temp_name = f"{str(self.backend_address)}.png"

            else:
                print(f"No Valid Backend Address Detected: {self.backend_address}")

        else:
            temp_name = self.picture.name

        try:

            time_taken, analyzed, number_capillaries, area_of_capillaries, segmented_image_clean = classify_image(
                self.picture)

            self.classified = time_taken
            self.number_of_capillaries = number_capillaries
            self.capillary_area = area_of_capillaries

            new_image_io = BytesIO()
            analyzed.save(new_image_io, format='JPEG')

            self.analyzed_picture.save(
                temp_name,
                content=ContentFile(new_image_io.getvalue()),
                save=False
            )

            new_image_io_segmented = BytesIO()
            segmented_image_clean.save(new_image_io_segmented, format='JPEG')

            self.segmented_image.save(
                temp_name,
                content=ContentFile(new_image_io_segmented.getvalue()),
                save=False
            )

            print(f'success: {self.classified}')

        except Exception as e:
            print("classification failed: ", traceback.format_exc())

        super(Image, self).save(*args, **kwargs)

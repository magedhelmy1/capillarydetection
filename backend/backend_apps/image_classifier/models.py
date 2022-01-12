from django.db import models


# Create your models here.
class Image(models.Model):
    picture = models.ImageField(upload_to="microcirculation_images", blank=True)
    backend_address = models.IntegerField(blank=True, null=True)
    time_to_classify = models.CharField(max_length=200, blank=True)
    uploaded = models.DateTimeField(auto_now_add=True)
    analyzed_picture = models.ImageField(upload_to="analyzed_picture", blank=True)
    segmented_image = models.ImageField(upload_to="segmented_image", blank=True)
    capillary_area = models.CharField(max_length=200, blank=True)
    number_of_cap = models.IntegerField(blank=True)

    def __str__(self):
        return f"Image classfied at {self.uploaded.strftime('%Y-%m-%d %H:%M')}"

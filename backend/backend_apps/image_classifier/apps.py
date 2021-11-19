from django.apps import AppConfig


class ImageClassifierConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api.Image'
    default = False

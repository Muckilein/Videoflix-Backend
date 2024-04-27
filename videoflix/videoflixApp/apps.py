from django.apps import AppConfig


class VideoflixappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'videoflixApp'
    
    def ready(self):
       from . import signals
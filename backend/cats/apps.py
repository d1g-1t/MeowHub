from django.apps import AppConfig


class CatsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cats'

    def ready(self):
        from . import signals  # noqa: F401

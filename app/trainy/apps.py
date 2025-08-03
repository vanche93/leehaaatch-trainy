from django.apps import AppConfig


class TrainyConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'trainy'
    verbose_name = 'Тренировки'

    def ready(self):
        import trainy.signals
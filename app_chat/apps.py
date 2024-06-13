from django.apps import AppConfig


class AppChatConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_chat'
    def ready(self):
        import app_chat.signals
from importlib import import_module

from django.apps import AppConfig as BaseAppConfig


class AppConfig(BaseAppConfig):

    name = "deep_vocabulary"

    def ready(self):
        import_module("deep_vocabulary.receivers")

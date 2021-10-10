from django.apps import AppConfig


class OptifolioConfig(AppConfig):
    name = 'optifolio'
    
    def ready(self):
        import optifolio.signals
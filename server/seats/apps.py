from django.apps import AppConfig


class SeatsConfig(AppConfig):
    name = 'seats'
    def ready(self):
        import seats.signals

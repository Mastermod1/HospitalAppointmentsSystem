from django.apps import AppConfig


class VisitRegistrationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'visit_registration'

    def ready(self):
        import visit_registration.signals

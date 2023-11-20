from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CirclesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "c_ride.circles"
    verbose_name = _("Circles")

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class RidesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "c_ride.rides"
    verbose_name = _("Rides")

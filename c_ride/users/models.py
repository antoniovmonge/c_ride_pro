from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db.models import BooleanField, CharField, EmailField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from c_ride.users.managers import UserManager
from c_ride.utils.models import CRideModel


class User(CRideModel, AbstractUser):
    """
    Default custom user model for c_ride.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    # First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore
    last_name = None  # type: ignore
    email = EmailField(_("email address"), unique=True)
    username = None  # type: ignore

    phone_regex = RegexValidator(
        regex=r"^\+?1?\d{9,15}$",
        message=_(
            "Phone number must be entered in the format: '+999999999'."
            "Up to 15 digits allowed."
        ),
    )
    phone_number = CharField(
        _("Phone number"), validators=[phone_regex], blank=True, max_length=17
    )
    phone_number_verified = BooleanField(
        _("Phone number verified"), default=False
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    is_client = BooleanField(
        "client status",
        default=True,
        help_text=(
            "Help easily distinguish users and perform queries."
            "Clients are the main type of user."
        ),
    )

    objects = UserManager()

    def get_absolute_url(self) -> str:
        """Get URL for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"pk": self.id})

    def __str__(self) -> str:
        """Return username."""
        return self.email

    def get_short_name(self) -> str:
        """Return username."""
        return self.email

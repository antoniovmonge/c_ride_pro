"""Circle invitation managers."""

# Django
# Utilities
import random
from string import ascii_uppercase, digits

from django.db import models


class InvitationManager(models.Manager):
    """Invitation manager.

    Used to handle code creation.
    """

    CODE_LENGTH = 6

    CODE_CHARS = ascii_uppercase + digits

    def create(self, **kwargs):
        """Handle code creation."""
        pool = kwargs.get("pool")
        if not pool:
            pool = self.CODE_CHARS
        code = self.create_code()
        while self.filter(code=code).exists():
            code = self.create_code()
        kwargs["code"] = code
        return super().create(**kwargs)

    def create_code(self):
        """Create a random code."""
        return "".join(random.choices(self.CODE_CHARS, k=self.CODE_LENGTH))

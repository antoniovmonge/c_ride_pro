# Django
import time

# Utilities
from datetime import timedelta

import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone

# Celery
from config import celery_app

User = get_user_model()


@celery_app.task()
def get_users_count():
    """A pointless Celery task to demonstrate usage."""
    return User.objects.count()


def gen_verification_token(user):
    """Create JWT token that the user can use to verify its account."""
    expiration_date = timezone.now() + timedelta(days=3)
    payload = {
        "user": user.name,
        "exp": int(expiration_date.timestamp()),
        "type": "email_confirmation",
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
    return token


@celery_app.task(name="send_confirmation_email", max_retries=3)
def send_confirmation_email(user_pk):
    """Send account verification link to given user."""
    for i in range(30):
        time.sleep(1)
        print("Sleeping", str(i + 1))
    user = User.objects.get(pk=user_pk)
    verification_token = gen_verification_token(user)
    subject = (
        f"Welcome @{user.username}! Verify your account to start using C_Ride"
    )
    from_email = "C_Ride <noreply@c_ride.com>"
    to = user.email
    content = render_to_string(
        "emails/users/account_verification.html",
        {"token": verification_token, "user": user},
    )
    msg = EmailMultiAlternatives(subject, content, from_email, [to])
    msg.attach_alternative(content, "text/html")
    msg.send()

"""Users serializers."""

# Utilities
from datetime import timedelta

import jwt
from django.conf import settings

# Django
from django.contrib.auth import authenticate, password_validation
from django.core.mail import EmailMultiAlternatives
from django.core.validators import RegexValidator
from django.template.loader import render_to_string
from django.utils import timezone

# Django REST Framework
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator

# Models
from c_ride.users.models import Profile, User

# Serializers
from c_ride.users.serializers.profiles import ProfileModelSerializer


class UserModelSerializer(serializers.ModelSerializer):
    """User model serializer."""

    profile = ProfileModelSerializer(read_only=True)

    class Meta:
        """Meta class."""

        model = User
        fields = (
            "name",
            "email",
            "phone_number",
            "profile",
        )


class UserLoginSerializer(serializers.Serializer):
    """User login serializer.

    Handle the login request data.
    """

    email = serializers.EmailField()
    password = serializers.CharField(min_length=8, max_length=64)

    def validate(self, data):
        """Check credentials."""
        user = authenticate(username=data["email"], password=data["password"])
        if not user:
            raise serializers.ValidationError("Invalid credentials")
        if not user.is_verified:
            raise serializers.ValidationError("Account is not active yet :(")
        self.context["user"] = user
        return data

    def create(self, data):
        """Generate or retrieve new token."""
        token, created = Token.objects.get_or_create(user=self.context["user"])
        return self.context["user"], token.key


class UserSignUpSerializer(serializers.Serializer):
    """User sign up serializer.

    Handle sign up data validation and user/profile creation.
    """

    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    # Phone number
    phone_regex = RegexValidator(
        regex=r"\+?1?\d{9,15}$",
        message="Phone number must be entered in the format: +999999999. Up to 15 digits allowed.",
    )
    phone_number = serializers.CharField(validators=[phone_regex])
    # Password
    password = serializers.CharField(min_length=8, max_length=64)
    password_confirmation = serializers.CharField(min_length=8, max_length=64)
    # Name
    name = serializers.CharField(min_length=2, max_length=30)
    # Picture
    picture = serializers.ImageField(
        required=False
    )  # required=False because it's not mandatory in the model

    def validate(self, data):
        """Verify passwords match."""
        password = data["password"]
        password_conf = data["password_confirmation"]
        if password != password_conf:
            raise serializers.ValidationError("Passwords don't match.")
        password_validation.validate_password(password)
        # We return the data dictionary once it's validated
        return data

    def create(self, data):
        """Handle user and profile creation."""
        data.pop("password_confirmation")
        user = User.objects.create_user(
            **data,
            is_verified=False,
            is_client=True,
        )
        Profile.objects.create(user=user)
        self.send_confirmation_email(user)
        return user

    def send_confirmation_email(self, user):
        """Send account verification link to given user."""
        verification_token = self.gen_verification_token(user)
        subject = f"Welcome @{user.username}! Verify your account to start using C_Ride"
        from_email = "C_Ride <noreply@c_ride.com>"
        to = user.email
        content = render_to_string(
            "emails/users/account_verification.html",
            {"token": verification_token, "user": user},
        )
        msg = EmailMultiAlternatives(subject, content, from_email, [to])
        msg.attach_alternative(content, "text/html")
        msg.send()

    def gen_verification_token(self, user):
        """Create JWT token that the user can use to verify its account."""
        expiration_date = timezone.now() + timedelta(days=3)
        payload = {
            "user": user.name,
            "exp": int(expiration_date.timestamp()),
            "type": "email_confirmation",
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
        return token


class AccountVerificationSerializer(serializers.Serializer):
    """Account verification serializer."""

    token = serializers.CharField()

    def validate_token(self, data):
        """Verify token is valid."""
        try:
            payload = jwt.decode(
                data, settings.SECRET_KEY, algorithms=["HS256"]
            )
        except jwt.ExpiredSignatureError:
            raise serializers.ValidationError("Verification link has expired.")
        except jwt.PyJWTError:
            raise serializers.ValidationError("Invalid token.")
        if payload["type"] != "email_confirmation":
            raise serializers.ValidationError("Invalid token.")
        self.context["payload"] = payload
        return data

    def save(self):
        """Update user's verified status."""
        payload = self.context["payload"]
        user = User.objects.get(name=payload["user"])
        user.is_verified = True
        user.save()

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, RedirectView, UpdateView

# Django REST Framework
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action

# Permissions
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

# Models
from c_ride.circles.models import Circle
from c_ride.circles.serializers import CircleModelSerializer
from c_ride.users.permissions import IsAccountOwner

# Serializers
from c_ride.users.serializers import (
    AccountVerificationSerializer,
    ProfileModelSerializer,
    UserLoginSerializer,
    UserModelSerializer,
    UserSignUpSerializer,
)

User = get_user_model()


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    slug_field = "id"
    slug_url_kwarg = "id"


user_detail_view = UserDetailView.as_view()


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    fields = ["name"]
    success_message = _("Information successfully updated")

    def get_success_url(self):
        assert (
            self.request.user.is_authenticated
        )  # for mypy to know that the user is authenticated
        return self.request.user.get_absolute_url()

    def get_object(self):
        return self.request.user


user_update_view = UserUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail", kwargs={"pk": self.request.user.pk})


user_redirect_view = UserRedirectView.as_view()


class UserViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    """User view set.

    Handle sign up, login and account verification.
    """

    queryset = User.objects.filter(is_active=True, is_client=True)
    serializer_class = UserModelSerializer
    lookup_field = "name"

    def get_permissions(self):
        """Assign permissions based on action."""
        if self.action in ["signup", "login", "verify"]:
            permissions = [AllowAny]
        elif self.action in ["retrieve", "update", "partial_update"]:
            permissions = [IsAuthenticated, IsAccountOwner]
        else:
            permissions = [IsAuthenticated]
        return [permission() for permission in permissions]

    @action(detail=False, methods=["post"])
    def login(self, request):
        """User sign in."""
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, token = serializer.save()
        data = {
            "user": UserModelSerializer(user).data,
            "access_token": token,
        }
        return Response(data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["post"])
    def signup(self, request):
        """User sign up."""
        serializer = UserSignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = UserModelSerializer(user).data
        return Response(data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["post"])
    def verify(self, request):
        """Account verification."""
        serializer = AccountVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {"message": _("Congratulation, now go share some rides!")}
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["put", "patch"])
    def profile(self, request, *args, **kwargs):
        """Update profile data."""
        user = self.get_object()
        profile = user.profile
        partial = request.method == "PATCH"
        serializer = ProfileModelSerializer(
            profile, data=request.data, partial=partial
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = UserModelSerializer(user).data
        return Response(data)

    def retrieve(self, request, *args, **kwargs):
        """Add extra data to the response."""
        response = super().retrieve(request, *args, **kwargs)
        circles = Circle.objects.filter(
            members=request.user, membership__is_active=True
        )
        data = {
            "user": response.data,
            "circles": CircleModelSerializer(circles, many=True).data,
        }
        response.data = data
        return response

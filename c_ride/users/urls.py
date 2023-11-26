# Django
from django.urls import include, path

# Django REST Framework
from rest_framework.routers import DefaultRouter

# Views
from c_ride.users.views import (
    user_detail_view,
    user_redirect_view,
    user_update_view,
)
from c_ride.users.views import users as user_views

app_name = "users"

router = DefaultRouter()
router.register(r"", user_views.UserViewSet, basename="users")


urlpatterns = [
    path("", include((router.urls, app_name))),
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("~update/", view=user_update_view, name="update"),
    path("<int:pk>/", view=user_detail_view, name="detail"),
]

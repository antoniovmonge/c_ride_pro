from django.urls import path

from c_ride.users.views import (
    UserLoginAPIView,
    user_detail_view,
    user_redirect_view,
    user_update_view,
)

app_name = "users"
urlpatterns = [
    path("login", UserLoginAPIView.as_view(), name="login"),
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("~update/", view=user_update_view, name="update"),
    path("<int:pk>/", view=user_detail_view, name="detail"),
]

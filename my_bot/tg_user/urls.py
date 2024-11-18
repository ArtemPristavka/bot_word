from django.urls import path

from .views import HaveTelegramUser, CreateTelegramUser


urlpatterns = [
    path("users/", CreateTelegramUser.as_view(), name="create-user"),
    path("users/<int:tg_id>/", HaveTelegramUser.as_view(), name="telegram-user"),
]
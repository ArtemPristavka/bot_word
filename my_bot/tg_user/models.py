from django.db import models
from django.contrib.auth.models import User


class TelegramUser(models.Model):
    "Модель содержит информаю о пользователе из Telegram"
    
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="telegram",
        auto_created=True
    )
    telegram_id = models.CharField(
        max_length=150,
        unique=True,
        blank=False
    )
    count_call = models.IntegerField(
        default=0
    )

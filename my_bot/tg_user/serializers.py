from rest_framework import serializers

from django.contrib.auth.models import User

from .models import TelegramUser


class TelegramUserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, min_length=4)
    telegram_id = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=150, min_length=8)
    
    def save(self, **kwargs) -> TelegramUser:
        """
        Для создания и сохранения в двух таблицах TelegramUser и User
        со связью

        Returns:
            TelegramUser:
        """
        user = User.objects.create_user(
            username=self.data.get("username"), # type: ignore
            password=self.data.get("password")
        )
        
        tg_user = TelegramUser.objects.create(
            user=user,
            telegram_id=str(self.data.get("telegram_id"))
        )
        
        return tg_user

    
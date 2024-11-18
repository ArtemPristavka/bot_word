from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework import status

from .models import TelegramUser

from .serializers import TelegramUserSerializer

from typing import Literal



class HaveTelegramUser(APIView):
    
    def get_object(self, tg_id: int) -> TelegramUser | Literal[False]:
        """
        Функция для получения объекта если он существует

        Args:
            tg_id (int): id пользователя из Telegram

        Raises:
            NotFound: Если пользователь не найден

        Returns:
            TelegramUser | Literal[False]: Объект пользователя или ничего
        """
        
        try:
            tg_user = TelegramUser.objects.select_related("user") \
                .get(telegram_id=str(tg_id))
                
        except: # TODO Добавить/разобрать ошибку DoesNotExist
            raise NotFound(
                detail="Not exists user telegram id",
                code=status.HTTP_404_NOT_FOUND
                )

        else:
            return tg_user
        
    def get(self, request: Request, tg_id: int) -> Response:
        """
        Для получения пользователя по его id Telegram

        Args:
            request (Request): 
            tg_id (int): id пользователя Telegram

        Returns:
            Response: 
        """
        
        tg_user = self.get_object(tg_id)
            
        reponse = {
            "username": tg_user.user.username, # type: ignore
            "telegram_id": int(tg_user.telegram_id), # type: ignore
            "count_call": tg_user.count_call # type: ignore
        }
        
        return Response(
            data=reponse,
            status=status.HTTP_200_OK
        )
        

    def put(self, request: Request, tg_id: int) -> Response:
        """
        Для обновления кол-во обращений пользователя

        Args:
            request (Request): 
            tg_id (int): id пользоваетеля Telegram

        Returns:
            Response: 
        """
        tg_user: TelegramUser = self.get_object(tg_id) # type: ignore
        tg_user.count_call += 1
        tg_user.save()
        
        reponse = {
            "username": tg_user.user.username, # type: ignore
            "telegram_id": int(tg_user.telegram_id), # type: ignore
            "count_call": tg_user.count_call # type: ignore
        }
        
        return Response(
            data=reponse,
            status=status.HTTP_200_OK
        )
        

class CreateTelegramUser(APIView):
    
    def post(self, request: Request) -> Response:
        """
        Создает пользователя 

        Args:
            request (Request): 

        Raises:
            ValidationError: 

        Returns:
            Response: 
        """
        
        serializer = TelegramUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            
            return Response(
                data={
                    "username": serializer.data.get("username"),
                    "telegram_id": int(serializer.data.get("telegram_id")),
                    "count_call": serializer.data.get("count_call")
                },
                status=status.HTTP_201_CREATED
            )
        
        else:
            raise ValidationError("Valid Error")
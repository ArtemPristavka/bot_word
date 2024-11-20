from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework import status
from .models import TelegramUser, CallTask
from .serializers import TelegramUserSerializer
from datetime import date
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
            "admin": tg_user.user.is_staff, # type: ignore
            "telegram_id": int(tg_user.telegram_id), # type: ignore
            "subscription": tg_user.subscription, # type: ignore
            "count_call":  CallTask.objects \
                .filter(user=tg_user.user.pk) \
                .count()# type: ignore
        }
        
        return Response(
            data=reponse,
            status=status.HTTP_200_OK
        )
        

    def post(self, request: Request, tg_id: int) -> Response:
        """
        Для обновления кол-во обращений пользователя

        Args:
            request (Request): 
            tg_id (int): id пользоваетеля Telegram

        Returns:
            Response: 
        """
        
        tg_user: TelegramUser = self.get_object(tg_id) # type: ignore
        CallTask.objects.create(user=tg_user.user)
        reponse = {
            "username": tg_user.user.username, # type: ignore
            "telegram_id": int(tg_user.telegram_id), # type: ignore
            "count_call": CallTask.objects \
                .filter(user=tg_user.user.pk) \
                .count() # type: ignore
        }
        
        return Response(
            data=reponse,
            status=status.HTTP_201_CREATED
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
                    "username": serializer.data.get("username"), # type: ignore
                    "telegram_id": int(serializer.data.get("telegram_id")), # type: ignore
                },
                status=status.HTTP_201_CREATED
            )
        
        else:
            return Response(
                data="User of have",
                status=status.HTTP_400_BAD_REQUEST
            )
    

class CountCall(APIView):
    
    def get(self, request: Request, year: int, month: int, day: int) -> Response:
        """
        Подсчет кол-во запросов в определнную дату

        Args:
            request (Request):
            year (int): 
            month (int):
            day (int):

        Returns:
            Response:
        """
        
        search_date = date(year=year, month=month, day=day)
        count_call = CallTask.objects.filter(date_call__date=search_date) \
            .count()
            
        return Response(
            data={
                "count_call": count_call,
            },
            status=status.HTTP_200_OK
        )
        

class MinDate(APIView):
    
    def get(self, request: Request) -> Response:
        """
        Поиск самой старой даты обращения пользователя

        Args:
            request (Request): 

        Returns:
            Response: 
        """
        
        search = CallTask.objects.order_by("date_call")[0]
        
        return Response(
            data={
                "year": search.date_call.year,
                "month": search.date_call.month,
                "day": search.date_call.day
            },
            status=status.HTTP_200_OK
        )


class UpdateSubscription(APIView):
    
    def post(self, request: Request, tg_id: int) -> Response:
        """
        Оформление подписки на бота

        Args:
            request (Request): 
            tg_id (int): Id пользователя Telegram

        Returns:
            Response: 
        """
        
        user = TelegramUser.objects.get(telegram_id=tg_id)
        user.subscription = True
        user.save()
        
        return Response(
            data="Made subscription",
            status=status.HTTP_201_CREATED
        )

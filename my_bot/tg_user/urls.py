from django.urls import path
from .views import (
    HaveTelegramUser, 
    CreateTelegramUser, 
    CountCall, 
    MinDate,
    UpdateSubscription  
)


urlpatterns = [
    path("users/", CreateTelegramUser.as_view(), name="create-user"),
    path("users/<int:tg_id>/", HaveTelegramUser.as_view(), name="telegram-user"),
    path("users/subscription/<int:tg_id>/", UpdateSubscription.as_view(), name="subscription"),
    path(
        "statistic/<int:year>/<int:month>/<int:day>/", 
        CountCall.as_view(), 
        name="statistic"
        ),
    path("date/", MinDate.as_view(), name="get-min-date"),
    
]
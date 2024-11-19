import requests

from typing import Dict


def get_min_date() -> Dict[str, int]:
    """
    Запрашиваем старую дату

    Returns:
        Dict[str, int]: _description_
    """
    request = requests.get(
        f"http://127.0.0.1:8000/telegram/date/"
    )
    response = {
        "year": request.json()["year"],
        "month": request.json()["month"],
        "day": request.json()["day"]
    }
    
    return response
    
def get_statistic(month: int, day: int, year: int = 2024) -> int:
    """
    Запрашиваем кол-во запросов пользователей в определнный день

    Args:
        month (int): месяц поиска
        day (int): день поиска
        year (int, optional): год поиска Defaults to 2024.

    Returns:
        int: кол-во запросов пользователей
    """
    
    request = requests.get(
        f"http://127.0.0.1:8000/telegram/statistic/{year}/{month}/{day}/"
    )
    count_call = request.json()["count_call"]
    
    return count_call


def register_user(username: str, password: str, telegram_id: int) -> bool:
    """
    Регистрация пользователя в системе

    Args:
        username (str):
        password (str):
        telegram_id (int):

    Returns:
        bool:
    """
    request = requests.post(
            url="http://127.0.0.1:8000/telegram/users/",
            data={
                "username": username,
                "password": password,
                "telegram_id": telegram_id
            }
        )
    return True if request.status_code == 201 else False
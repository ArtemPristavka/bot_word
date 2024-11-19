import requests


class User:
    "Класс описывающий пользователя"
    
    _have = None
    _admin = None
    _username = None
    _count_call = None
    
    def __init__(self, telegram_id: int) -> None:
        self._telegram_id = telegram_id
        self.request_user()
        
    def request_user(self) -> None:
        "Проверяем есть ли такой пользователь в системе"
        
        check_user = requests.get(
            f"http://127.0.0.1:8000/telegram/users/{self.telegram_id}/"
            )
        
        if check_user.status_code == 200:
            self._have = True
            self._admin = check_user.json()["admin"]
            self._username = check_user.json()["username"]
            self._count_call = check_user.json()["count_call"]
            
        elif check_user.status_code == 404:
            self._have = False
            
    def send_call(self) -> None:
        "Сообщаем системе что пользователь воспользовался задачей"
        
        send = requests.post(
            f"http://127.0.0.1:8000/telegram/users/{self.telegram_id}/"
        )
        if send.status_code == 201:
            self._count_call = send.json()["count_call"]
    
    
    @property
    def count_call(self) -> int | None:
        "Кол-во обращей пользователя"
        
        return self._count_call
    
    @property
    def have(self) -> bool:
        "Наличие пользователя в системе"
        
        return self._have # type: ignore
    
    @have.setter
    def have(self, value: bool) -> None:
        self._have = value
    
    @property
    def admin(self) -> None | bool:
        "Является ли пользователь админом"
        
        if self._have is False:
            return None
        return self._admin
    
    @admin.setter
    def admin(self, value: bool) -> None:
        self._admin = value
    
    @property
    def username(self) -> None | str:
        "Ник пользователя"
        
        if self._have is False:
            return None
        return self._username
    
    @username.setter
    def username(self, value: str) -> None:
        self._username = value
        
    @property
    def telegram_id(self) -> int:
        "Id пользователя в Telegram"
        return self._telegram_id
    
    @telegram_id.setter
    def telegram_id(self, value: int) -> None:
        self._telegram_id = value
        
        
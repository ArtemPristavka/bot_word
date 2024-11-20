import requests


class User:
    "Класс описывающий пользователя"
    
    _have = None
    _admin = None
    _username = None
    _count_call = None
    _subscription = None
    
    def __init__(self, telegram_id: int) -> None:
        self._telegram_id = telegram_id
        self.request_user()
        
    def request_user(self) -> None:
        "Проверяем есть ли такой пользователь в системе"
        
        user = requests.get(
            f"http://127.0.0.1:8000/telegram/users/{self.telegram_id}/"
            )
        
        if user.status_code == 200:
            self.have = True
            self.admin = user.json()["admin"]
            self.username = user.json()["username"]
            self.count_call = user.json()["count_call"]
            self.subscription = user.json()["subscription"]
            
        elif user.status_code == 404:
            self.have = False
            
    def send_call(self) -> None:
        "Сообщаем системе что пользователь воспользовался задачей"
        
        send = requests.post(
            f"http://127.0.0.1:8000/telegram/users/{self.telegram_id}/"
        )
        if send.status_code == 201:
            self.count_call = send.json()["count_call"]
            
    def send_subscription(self) -> bool | None:
        "Отправляем подписку"
        
        request = requests.post(
            f"http://127.0.0.1:8000/telegram/users/subscription/{self._telegram_id}/"
        )
        if request.status_code == 201:
            self._subscription = True
        
        else:
            self._subscription = False
        
        return self.subscription
    
    @property
    def subscription(self) -> bool | None:
        return self._subscription
    
    @subscription.setter
    def subscription(self, value) -> None:
        self._subscription = value
    
    @property
    def count_call(self) -> int | None:
        "Кол-во обращей пользователя"
        
        return self._count_call
    
    @count_call.setter
    def count_call(self, value) -> None:
        self._count_call = value
    
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
        
        
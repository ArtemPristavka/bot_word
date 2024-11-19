import requests


class CheckUser:
    
    def __init__(self, telegram_id: int) -> None:
        self._telegram_id = telegram_id
        self.request_user()
        
    def request_user(self) -> None:
        check_user = requests.get(
            f"http://127.0.0.1:8000/telegram/users/{self._telegram_id}/"
            )
        if check_user.status_code == 200:
            self._have = True
            self._admin = check_user.json()["admin"]
            self._username = check_user.json()["username"]
        elif check_user.status_code == 404:
            self._have = False
            
    @property
    def have(self) -> bool:
        return self._have
    
    @have.setter
    def have(self, value: bool) -> None:
        self._have = value
    
    @property
    def admin(self) -> None | bool:
        if self._have is False:
            return None
        return self._admin
    
    @admin.setter
    def admin(self, value: bool) -> None:
        self._admin = value
    
    @property
    def username(self) -> None | str:
        if self._have is False:
            return None
        return self._username
    
    @username.setter
    def username(self, value: str) -> None:
        self._username = value
        
    @property
    def telegram_id(self) -> int:
        return self._telegram_id
    
    @telegram_id.setter
    def telegram_id(self, value: int) -> None:
        self._telegram_id = value
        
        
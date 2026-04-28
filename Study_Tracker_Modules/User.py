import hashlib
from logging import raiseExceptions


class User:
    def __init__(self, user_id: int, name: str, email: str, password: str):
        if user_id < 0:
            raise ValueError("User id cannot be negative")
        elif not name:
            raise ValueError("Name cannot be empty")
        elif not email:
            raise ValueError("Email cannot be empty")
        elif not password:
            raise ValueError("Password cannot be empty")
        else:
            self.__user_id: int = user_id
            self.__name: str = name
            self.__email: str = email
            self.__password: str = password

    @property
    def user_id(self):
        return self.__user_id

    @user_id.setter
    def user_id(self, value):
        if value < 0:
            raise ValueError
        else:
            self.__user_id = value

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value.lower()

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, value):
        self.__email = value.lower()

    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, value):
        self.__password = value

    def change_password(self, new_password, old_password) -> bool:
        new_password = self.password_hasher(new_password)
        old_password = self.password_hasher(old_password)
        if old_password != new_password and old_password == self.password:
             self.password = new_password
             return True
        else:
            return False

    @staticmethod
    def password_hasher(password: str) -> str:
        password = hashlib.sha256(password.encode()).hexdigest()
        return password


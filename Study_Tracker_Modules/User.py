import hashlib


class User:
    def __init__(self, user_id: int, name: str, password: str):
        if user_id < 0:
            raise ValueError("User id cannot be negative")
        elif not name:
            raise ValueError("Name cannot be empty")
        elif not password:
            raise ValueError("Password cannot be empty")
        else:
            self.__user_id: int = user_id
            self.__name: str = name.lower()
            self.__password: str = password

    @property
    def user_id(self) -> int:
        return self.__user_id

    @user_id.setter
    def user_id(self, value: int) -> None:
        if value < 0:
            raise ValueError
        else:
            self.__user_id = value

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str) -> None:
        if not value:
            raise ValueError("Name cannot be empty")
        else:
            self.__name = value.lower()

    @property
    def password(self) -> str:
        return self.__password

    @password.setter
    def password(self, value: str) -> None:
        if not value:
            raise ValueError("Password cannot be empty")
        else:
            self.__password = value


    def change_password(self, new_password: str, old_password: str) -> bool:
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

    @staticmethod
    def login( name, password) -> User:

        return User(1,name,password)


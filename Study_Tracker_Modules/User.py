



class User:
    def __init__(self, name: str, email: str, password: str):
        self.__name: str = name
        self.__email: str = email
        self.__password: str = password

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
        if old_password != new_password and old_password == self.password:
             self.password = new_password
             return True
        else:
            return False

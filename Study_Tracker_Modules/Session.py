from datetime import datetime

STUDY_TYPES: list = ["reading","reviewing","watching","project work","coding","research"]

class Session:
    def __init__(self, session_id: int, subject_name: str, date: datetime, session_time: float, study_type: str, subject_id: int, user_id: int):
        if session_id < 0:
            raise Exception('Session id cannot be negative')
        # TODO fix this, needs to be date
        # elif date != type(datetime):
        #     raise Exception('Date must be of type datetime')
        elif session_time < 0:
            raise Exception('Session time cannot be negative')
        elif study_type.lower() not in STUDY_TYPES:
            raise Exception('Study type must be one of ' + ', '.join(STUDY_TYPES))
        elif subject_id < 0:
            raise Exception('Subject id cannot be negative')
        elif user_id < 0:
            raise Exception('User id cannot be negative')
        else:
            self.__session_id = session_id
            self.__date = date.date()
            self.__session_time = session_time
            self.__study_type = study_type.lower()
            self.__subject_name = subject_name
            self.__subject_id = subject_id
            self.__user_id = user_id

    @property
    def session_id(self) -> int:
        return self.__session_id

    @session_id.setter
    def session_id(self, value: int) -> None:
        if value < 0:
            raise Exception('Session id cannot be negative')
        else:
            self.__session_id = value

    @property
    def subject_name(self) -> str:
        return self.__subject_name

    @subject_name.setter
    def subject_name(self, value: str) -> None:
        if value:
            self.__subject_name = value
        else:
            raise Exception('Subject name cannot be empty')

    # TODO need to assign date properly
    @property
    def date(self):
        return self.__date

    @date.setter
    def date(self, value: datetime) -> None:
        if type(value) != datetime:
            raise Exception('Date must be of type datetime')
        else:
            self.__date = value

    @property
    def session_time(self) -> float:
        return self.__session_time

    @session_time.setter
    def session_time(self, value: float) -> None:
        if value < 0:
            raise Exception('Session time cannot be negative')
        else:
            self.__session_time = value

    @property
    def study_type(self) -> str:
        return self.__study_type

    @study_type.setter
    def study_type(self, value: str) -> None:
        if value not in STUDY_TYPES:
            raise Exception('Study type must be one of ' + ', '.join(STUDY_TYPES))
        else:
            self.__study_type = value

    @property
    def subject_id(self) -> int:
        return self.__subject_id

    @subject_id.setter
    def subject_id(self, value: int) -> None:
        if value < 0:
            raise Exception('Subject id cannot be negative')
        else:
            self.__subject_id = value

    @property
    def user_id(self) -> int:
        return self.__user_id

    @user_id.setter
    def user_id(self, value: int) -> None:
        if value < 0:
            raise Exception('User id cannot be negative')
        else:
            self.__user_id = value

    def __str__(self):
        obj_state: str = ""

        obj_state = f"Session ID: {self.session_id}\n"
        obj_state += f"Subject Name: {self.subject_name}\n"
        obj_state += f"Date: {self.date}\n"
        obj_state += f"Session Time: {self.session_time:.2f}\n"
        obj_state += f"Study Type: {self.study_type}\n"
        obj_state += f"Subject ID: {self.subject_id}\n"
        obj_state += f"User ID: {self.user_id}"

        return obj_state





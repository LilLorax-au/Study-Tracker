



class Subject:
    def __init__(self, subject_id, name: str, description: str, weekly_recommended_hours: int, difficulty: int):
        if subject_id < 0:
            raise ValueError("Subject id cannot be negative")
        elif not name:
            raise ValueError("Subject name cannot be empty")
        elif not description:
            raise ValueError("Subject description cannot be empty")
        elif weekly_recommended_hours < 0:
            raise ValueError("Weekly recommended hours cannot be negative")
        elif weekly_recommended_hours > (24*7):
            raise ValueError("Weekly recommended hours cannot be greater than a week")
        elif difficulty < 0:
            raise ValueError("Difficulty cannot be negative")
        elif difficulty > 10:
            raise ValueError("Difficulty cannot be greater than 10")
        else:
            self.__subject_id = subject_id
            self.__name = name
            self.__description = description
            self.__weekly_recommended_hours = weekly_recommended_hours
            self.__difficulty = difficulty

    @property
    def subject_id(self):
        return self.__subject_id

    @subject_id.setter
    def subject_id(self, subject_id):
        if subject_id < 0:
            raise ValueError("Subject id cannot be negative")
        else:
            self.__subject_id = subject_id

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        if not name:
            raise ValueError("Subject name cannot be empty")
        else:
            self.__name = name

    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self, description):
        if not description:
            raise ValueError("Subject description cannot be empty")
        else:
            self.__description = description

    @property
    def weekly_recommended_hours(self):
        return self.__weekly_recommended_hours

    @weekly_recommended_hours.setter
    def weekly_recommended_hours(self, weekly_recommended_hours):
        if weekly_recommended_hours < 0:
            raise ValueError("Weekly recommended hours cannot be negative")
        elif weekly_recommended_hours > (24*7):
            raise ValueError("Weekly recommended hours cannot be greater than a week")
        else:
            self.__weekly_recommended_hours = weekly_recommended_hours

    @property
    def difficulty(self):
        return self.__difficulty

    @difficulty.setter
    def difficulty(self, difficulty):
        if difficulty < 0:
            raise ValueError("Difficulty cannot be negative")
        elif difficulty > 10:
            raise ValueError("Difficulty cannot be greater than 10")
        else:
            self.__difficulty = difficulty
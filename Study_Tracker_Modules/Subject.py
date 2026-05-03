



class Subject:
    def __init__(self, subject_id: int, name: str, description: str, weekly_goal_hours: int, difficulty: int):
        if subject_id < 0:
            raise ValueError("Subject id cannot be negative")
        elif not name:
            raise ValueError("Subject name cannot be empty")
        elif not description:
            raise ValueError("Subject description cannot be empty")
        elif weekly_goal_hours < 0:
            raise ValueError("Subject Weekly goal hours cannot be negative")
        elif weekly_goal_hours > (24 * 7):
            raise ValueError("Subject Weekly goal hours cannot be greater than a week")
        elif difficulty < 0:
            raise ValueError("Subject Difficulty cannot be negative")
        elif difficulty > 10:
            raise ValueError("Subject Difficulty cannot be greater than 10")
        else:
            self.__subject_id: int = subject_id
            self.__name: str = name.lower()
            self.__description: str = description.lower()
            self.__weekly_goal_hours: int = weekly_goal_hours
            self.__difficulty: int = difficulty

    @property
    def subject_id(self) -> int:
        return self.__subject_id

    @subject_id.setter
    def subject_id(self, subject_id: int) -> None:
        if subject_id < 0:
            raise ValueError("Subject id cannot be negative")
        else:
            self.__subject_id = subject_id

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, name: str) -> None:
        if not name:
            raise ValueError("Subject name cannot be empty")
        else:
            self.__name = name

    @property
    def description(self) -> str:
        return self.__description

    @description.setter
    def description(self, description: str) -> None:
        if not description:
            raise ValueError("Subject description cannot be empty")
        else:
            self.__description = description

    @property
    def goal(self) -> int:
        return self.__weekly_goal_hours

    @goal.setter
    def goal(self, weekly_goal_hours: int) -> None:
        if weekly_goal_hours < 0:
            raise ValueError("Weekly recommended hours cannot be negative")
        elif weekly_goal_hours > (24 * 7):
            raise ValueError("Weekly recommended hours cannot be greater than a week")
        else:
            self.__weekly_goal_hours = weekly_goal_hours

    @property
    def difficulty(self) -> int:
        return self.__difficulty

    @difficulty.setter
    def difficulty(self, difficulty:int ) -> None:
        if difficulty < 0:
            raise ValueError("Difficulty cannot be negative")
        elif difficulty > 10:
            raise ValueError("Difficulty cannot be greater than 10")
        else:
            self.__difficulty = difficulty

    def __str__(self) -> str:
        obj_state: str = ""
        obj_state = f"Subject ID: {self.subject_id}\n"
        obj_state += f"Subject Name: {self.name}\n"
        obj_state += f"Subject Description: {self.description}\n"
        obj_state += f"Subject Weekly Goal: {self.goal}\n"
        obj_state += f"Subject Difficulty: {self.difficulty}"

        return obj_state
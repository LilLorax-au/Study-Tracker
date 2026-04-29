from datetime import datetime



class Stopwatch:
    def __init__(self):
        self.__start: datetime | None = None
        self.__end: datetime | None = None
        self.__counter: float = 0

    def start_time(self) -> datetime | None:
        self.__start = datetime.now()

    def stop_time(self) -> float:
        if self.__start is None:
            raise Exception('Start Time not set')
        else:
            self.__end = datetime.now()

        return self.__find_difference()

    def __find_difference(self) -> float:
        self.__counter = (self.__end - self.__start).total_seconds()
        value = self.__counter

        self.clear_all()

        return value

    def clear_all(self) -> None:
        self.__start = None
        self.__end = None
        self.__counter = 0


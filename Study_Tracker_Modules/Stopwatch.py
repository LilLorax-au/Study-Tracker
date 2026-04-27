from datetime import datetime



class Stopwatch:
    def __init__(self):
        self.__start: datetime = None
        self.__end: datetime = None
        self.__counter: float = 0

    def start_time(self):
        self.__start = datetime.now()

    def stop_time(self) -> float:
        self.__end = datetime.now()

        return self.__find_difference()

    def __find_difference(self):
        self.__counter = (self.__end - self.__start).total_seconds()
        return self.__counter
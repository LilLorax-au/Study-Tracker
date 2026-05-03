from Study_Tracker_Modules.Stopwatch import Stopwatch
from Study_Tracker_Modules.User import User
from Study_Tracker_Modules.Session import Session, STUDY_TYPES
from Study_Tracker_Modules.Subject import Subject
from datetime import datetime



LINE_SPLITTER = "-"*30


def main():
    data = load()

    welcome()
    if len(data["user"]) == 0:
        login_loop(data)
    if len(data["subjects"]) == 0:
        new_subjects(data)

    main_loop(data)



    return

def line_split(func):
    def wrapper(*args, **kwargs):
        print(LINE_SPLITTER)
        result = func(*args, **kwargs)
        print(LINE_SPLITTER)
        return result
    return wrapper

@line_split
def login_loop(data: dict) -> None:
    user: User | None = None
    name: str = ""
    password: str = ""

    while user is None:
        try:
            if not name:    
                name = input("Please enter your name: ")
                if not name:
                    raise ValueError("Name must not be blank")
            if not password:
                password = input("Please enter your password: ")
                if not password:
                    raise ValueError("Password must not be blank")
                user = User.login(name,password)
        except ValueError as error:
            print("Please enter a valid input, must fill all inputs & id must be a number" + " \n" + str(error))
    print("Logged in successfully")

    return

@line_split
def new_subjects(data: dict) -> None:
    exit_now = False
    name = ""
    description = ""
    goal = -1
    difficulty = -1
    error_counter = 0

    while not exit_now:
        if len(data["subjects"]) == 0 and error_counter == 0:
            print("Looks like you have no subjects, lets add some!")
        try:
            if not name:
                name = input("Please enter your subject's name: ")
                if not name:
                    raise ValueError("Subject name cannot be empty")
            if not description:
                description = input("Please enter your subject's description: ")
                if not description:
                    raise ValueError("Subject description cannot be empty")
            if goal == -1:
                try: 
                    goal = int(input("Please enter your subject's weekly study goal in hours: "))
                except ValueError as error:
                    error.args = ("Goal must be a integer",)
                    goal = -1
                    raise error
                else:
                    if goal < 0:
                        goal = -1
                        raise ValueError("Goal must be higher then 0")
                    elif goal > 84:
                        goal = -1
                        raise ValueError(f"That's unhealthy, make a more reasonable goal")
            if difficulty == -1:
                try:
                    difficulty = int(input("Please enter your subject's difficulty: "))
                except ValueError as error:
                    error.args=  ("Difficulty can only be an integer",)
                    difficulty = -1
                    raise error
                else:
                    if difficulty < 0 or difficulty > 10:
                        difficulty = -1
                        raise ValueError("Difficulty can only be between 0 and 10")

        except ValueError as error:
            print(str(error))
            error_counter += 1
            continue
        else:
            if len(data["subjects"]) == 0:
                data["subjects"].append(Subject(1, name, description, goal, difficulty))
            else:
                highest: int = 1
                for each in data["subjects"]:
                    if highest < each.subject_id:
                        highest = each.subject_id
                data["subjects"].append(Subject(highest + 1, name, description, goal, difficulty))

        if input("Another?(Y/N): ").lower() == "n":
            exit_now = True

@line_split
def main_loop(data):
    exit_now = False
    while not exit_now:
        user_input = input(
            "What would you like to do?\n"
            "start new session(Type: session)\n"
            "to see session data(Type: see sessions)\n"
            "to manage subjects(Type: update subject)\n"    
            "to manage user account(Type: user)\n"
            "to save and exit(Type: exit)\n")
        match user_input.lower():
            case "session":
                session_manager(data)
                print("made it")
                continue
            case "see sessions":
                continue
            case "update subject":
                update_subject(data)
                continue
            case "new subject":
                new_subjects(data)
                continue
            case "user":
                continue
            case "exit":
                continue
            case _:
                print(f"Invalid input: '{user_input}'\n ")
                continue

@line_split
def session_manager(data):
    exit_now = False
    session_type = ""
    subject_name = ""
    subject_id = 0
    start = ""

    timer = Stopwatch()

    while not exit_now:
        try:
            if not session_type:
                session_type = input("Please enter your session type: ")
                if session_type not in STUDY_TYPES:
                    session_type = ""
                    raise ValueError("Please enter a valid session type")

            if not subject_name:
                subject_name = input("Please enter your session's subject: ")

                subject_id = match_subject_name(subject_name, data).subject_id
                if subject_id is None:
                    subject_name = ""
                    raise ValueError("Please enter a valid subject")

            if not start:
                start = input("Please enter (start) to be begin: ")
                if start.lower() == "start":

                    timer.start_time()
                    input("When you're finished, just press enter ")
                    study_time = (timer.stop_time()/60)/60

                    if len(data["sessions"]) == 0:
                        data["sessions"].append(
                            Session(
                                1,
                                datetime.now(),
                                study_time,
                                session_type,
                                subject_id,
                                data["user"].user_id))
                    else:
                        data["sessions"].append(
                            Session(
                                data["sessions"].session_id + 1,
                                datetime.now(),
                                study_time,
                                session_type,
                                subject_id,
                                data["user"].user_id))
                    exit_now = True
                else:
                    start = ""
                    raise ValueError("Please only enter the work 'start'")
        except ValueError as error:
            print(error)

@line_split
def update_subject(data):
    exit_now: bool = False
    subject: Subject | None = None
    name: str = ""
    description: str = ""
    goal: int = -1
    difficulty: int = -1


    while not exit_now:
        try:
            if not name:
                name = input("Please enter the name of the subject to change: ")
                subject = match_subject_name(name, data)
                if subject is None:
                    name = ""
                    raise ValueError(f"'{name}' not found")
                else:
                    name = input(f"Current name: '{subject.name}'\nNew name: ")
                    if name:
                        subject.name = name.lower()
                    else:
                        raise ValueError("Name cannot be empty")

            if not description and subject is not None:
                description = input(f"Current description: '{subject.description}'\nNew description: ")
                if description:
                    subject.description = description
                else:
                    raise ValueError("Description cannot be empty")

            if goal is -1 and subject is not None:
                try:
                    goal = int(input(f"Current goal: {subject.goal}\nNew goal: "))
                except ValueError as error:
                    error.args = ("Goal must be a integer",)
                    goal = -1
                    raise error
                else:
                    if goal < 0:
                        goal = -1
                        raise ValueError("Goal must be higher then 0")
                    elif goal > 84:
                        goal = -1
                        raise ValueError(f"That's unhealthy, make a more reasonable goal")
                    else:
                        subject.goal = goal

            if difficulty is -1 and subject is not None:
                try:
                    difficulty = int(input(f"Current difficulty: {subject.difficulty}\nNew difficulty: "))
                except ValueError as error:
                    error.args = ("Difficulty must be a integer",)
                    difficulty = -1
                    raise error
                else:
                    if difficulty < 0 or difficulty > 10:
                        difficulty = -1
                        raise ValueError("Difficulty can only be between 0 and 10")
                    else:
                        subject.difficulty = difficulty


        except ValueError as error:
            print(error)
        else:
            print(f"{subject.name}'s new state:\n" + str(subject))
            exit_now = True


    return

def update_user(data):
    exit_now: bool = False
    user: User = data["user"][0]
    name: str = ""
    password: str = ""

    while not exit_now:
        try:
            if not name:
                name = input(f"Current name: {user.name}\nNew name: ")


@line_split
def welcome():
    print("Welcome to Study Tracker!")

# @line_split
# def save(data: dict):
#     success: bool
#     success = True
#
#     return success
@line_split
def load() -> dict:
    data = \
        {
            "user": [],
            "subjects": [],
            "sessions": []
        }
    return data

def match_subject_name(name: str, data: dict) -> Subject | None:

    for each in data["subjects"]:
        if each.name == name:
            return each
    return None

if __name__ == '__main__':
    main()
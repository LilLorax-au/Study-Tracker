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
        data["user"] = login_loop()
    if len(data["subjects"]) == 0:
        data["subjects"] = create_subjects()

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
def login_loop() -> User:
    user = None

    while user is None:
        try:
            name = input("Please enter your name: ")
            password = input("Please enter your password: ")
            email = input("Please enter your email: ")
            user_id = int(input("Please enter your user id: "))
            user = User(user_id, name, email, password)
        except ValueError as error:
            print("Please enter a valid input, must fill all inputs & id must be a number" + " \n" + str(error))
    print("Logged in successfully")

    return user

@line_split
def create_subjects() -> list[Subject]:
    exit_now = False
    subjects = []
    subject_id = -1
    name = ""
    description = ""
    goal = -1
    difficulty = -1
    error_counter = 0

    while not exit_now:
        if len(subjects) == 0 and error_counter == 0:
            print("Looks like you have no subjects, lets add some!")
        try:
            # TODO false error handing on ints
            if subject_id == -1:
                subject_id = int((input("Please enter your subject id: ")))
                if type(subject_id) is not int:
                    subject_id = -1
                    raise ValueError("ID can only be an integer")
            if not name:
                name = input("Please enter your subject's name: ")
                if not name:
                    raise ValueError("Subject name cannot be empty")
            if not description:
                description = input("Please enter your subject's description: ")
                if not description:
                    raise ValueError("Subject description cannot be empty")
            if goal == -1:
                goal = int(input("Please enter your subject's weekly study goal in hours: "))
                if type(goal) is not int:
                    goal = -1
                    raise ValueError("Goal can only be an integer")
            if difficulty == -1:
                difficulty = int(input("Please enter your subject's difficulty: "))
                if type(difficulty) is not int:
                    difficulty = -1
                    raise ValueError("Difficulty can only be an integer")
            try:
                subjects.append(Subject(subject_id, name, description, goal, difficulty))
            except ValueError as error:
                print(str(error))
                value = str(error).split(" ")[1]
                match value:
                    case "id":
                        subject_id = -1
                        break
                    case "name":
                        name = ""
                        break
                    case "description":
                        description = ""
                        break
                    case "goal":
                        goal = -1
                        break
                    case "difficulty":
                        difficulty = -1
                        break

        except ValueError as error:
            print(str(error))
            error_counter += 1
            continue

        if input("Another?(Y/N): ").lower() == "n":
            exit_now = True
    print(subjects[0])
    return subjects
@line_split
def main_loop(data):
    exit_now = False
    while not exit_now:
        user_input = input(
            "What would you like to do?\n"
            "start new session(Type: session)\n"
            "to see session data(Type: see sessions)"
            "to manage subjects(Type: subject)\n"    
            "to manage user account(Type: user)\n")
        match user_input.lower():
            case "session":
                session_manager(data)
                print("made it")
                continue
            case "see sessions":
                continue
            case "subject":
                continue
            case "user":
                continue

@line_split
def session_manager(data):
    exit_now = False
    session_type = ""
    subject = ""
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

            if not subject:
                subject = input("Please enter your session's subject: ")
                subject_id = match_subject_name(subject, data)
                if subject_id is None:
                    subject = ""
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

def match_subject_name(name: str, data: dict) -> None | int:

    for each in data["subjects"]:
        if each.name == name:
            return each.subject_id
    return None

if __name__ == '__main__':
    main()
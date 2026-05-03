import time

from Study_Tracker_Modules.Stopwatch import Stopwatch
from Study_Tracker_Modules.User import User
from Study_Tracker_Modules.Session import Session, STUDY_TYPES
from Study_Tracker_Modules.Subject import Subject
from Study_Tracker_Modules.Database import StudyTrackerDB
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd



LINE_SPLITTER = "-"*30


def main():
    db = StudyTrackerDB()

    data = load(db)

    welcome()

    login_loop(data)

    if len(data["subjects"]) == 0:
        new_subjects(data)

    main_loop(data, db)

    return

def line_split(func):
    """formatting decorator for outputs"""
    def wrapper(*args, **kwargs):
        print(LINE_SPLITTER)
        result = func(*args, **kwargs)
        print(LINE_SPLITTER)
        return result
    return wrapper

def welcome():
    """To print welcome message"""
    print("Welcome to Study Tracker!")

@line_split
def login_loop(data: dict) -> None:
    """logs in a user or signs up if there are no users"""
    user: User | None = None
    name: str = ""
    password: str = ""
    login_success: bool = False
    password_counter: int = 4
    shutdown_count: int = 3

    # call for if a user exists
    if len(data["user"]) > 0:
        while not login_success:
            try:
                if not name:
                    name = input("Please enter your name: ")
                    # look for user, user list at the point of 03/05/2026 should only ever hold one user.
                    for each in data["user"]:
                        if name.lower() == each.name:
                            user = each
                            break
                    if user is None:
                        name = ""
                        raise ValueError("Name not found")
                if user is not None:
                    password = input(f"Hello {user.name}, please enter your password: ")
                    # check if passwords match
                    if User.password_hasher(password) is not user.password:
                        password_counter -= 1
                        if password_counter == 0:
                            while shutdown_count:
                                print(f"Passwords do not match to many times: shutting down in {shutdown_count}")
                                time.sleep(1)
                                shutdown_count -= 1
                            exit()
                        else:
                            raise ValueError(f"Password not matched, Tries remaining: {password_counter}")
                    else:
                        login_success = True
            except ValueError as error:
                print(str(error))

    # call for if no user exists
    else:
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
            except ValueError as error:
                print("Please enter a valid input, must fill all inputs & id must be a number" + " \n" + str(error))
            else:
                user = User.sign_up(name, password)
                data["user"].append(user)

    print("Logged in successfully")
    return

@line_split
def new_subjects(data: dict) -> None:
    """Create new subject, adds to data dict"""
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
                # the first subject should have id of one
                data["subjects"].append(Subject(1, name, description, goal, difficulty))
            else:
                # finding the highest id stops any ids repeating
                highest: int = 1
                for each in data["subjects"]:
                    if highest < each.subject_id:
                        highest = each.subject_id
                data["subjects"].append(Subject(highest + 1, name, description, goal, difficulty))

        if input("Another?(Y/N): ").lower() == "n":
            exit_now = True
        else:
            name = ""
            description = ""
            goal = -1
            difficulty = -1
            error_counter = 0

@line_split
def main_loop(data, db):
    """Main program loop"""
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
                see_sessions(data)
                continue
            case "update subject":
                update_subject(data)
                continue
            case "new subject":
                new_subjects(data)
                continue
            case "user":
                update_user(data)
                continue
            case "exit":
                db.build_schema()
                db.save_data(data)
                exit_now = True
                continue
            case _:
                print(f"Invalid input: '{user_input}'\n ")
                continue

@line_split
def session_manager(data):
    """where sessions are made and ran"""
    exit_now = False
    session_type = ""
    subject_name = ""
    subject_id: int | None = 0
    start = ""

    timer = Stopwatch()

    while not exit_now:
        try:
            if not session_type:
                session_type = input("Please enter your session type: ")
                if session_type.lower() not in STUDY_TYPES:
                    session_type = ""
                    raise ValueError("Please enter a valid session type")

            if not subject_name:
                subject_name = input("Please enter your session's subject: ")

                if match_subject_name(subject_name, data) is not None:
                    subject_id = match_subject_name(subject_name, data).subject_id
                else:
                    subject_name = ""
                    raise ValueError("Please enter a valid subject")

            if not start:
                start = input("Please enter (start) to be begin: ")
                if start.lower() == "start":

                    timer.start_time()
                    input("When you're finished, just press enter ")
                    study_time = (timer.stop_time()/60)

                    if len(data["sessions"]) == 0:
                        data["sessions"].append(
                            Session(
                                1,
                                subject_name,
                                datetime.now(),
                                study_time,
                                session_type,
                                subject_id,
                                data["user"][0].user_id))
                    else:
                        highest: int = 1
                        for each in data["sessions"]:
                            if highest < each.session_id:
                                highest = each.session_id
                        data["sessions"].append(
                            Session(
                                highest + 1,
                                subject_name,
                                datetime.now(),
                                study_time,
                                session_type,
                                subject_id,
                                data["user"][0].user_id))
                    exit_now = True
                else:
                    start = ""
                    raise ValueError("Please only enter the work 'start'")
        except ValueError as error:
            print(error)
@line_split
def see_sessions(data):
    """Shows data visuals for sessions: just text at this point, ran out of time to complete visuals"""
    for each in data["sessions"]:
        print(each)



    # sessions: list = []
    # for each in data["sessions"]:
    #     sessions.append(
    #         [int(each.session_id),
    #          str(each.date),
    #          float(each.session_time),
    #          str(each.study_type)])
    #
    # df = pd.DataFrame(sessions, columns=["session_id", "date", "session_time", "study_type"])
    #
    # plt.plot(df)
    # plt.show()
@line_split
def update_subject(data):
    """update a subject"""
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

@line_split
def update_user(data):
    """update a user"""
    # README:: only ever one user at the point of 03/05/2026, if ever more users, refactor required

    exit_now: bool = False
    user: User = data["user"][0]
    name: str = ""
    password_counter: int = 3
    password_changed: bool = False


    while not exit_now:
        try:
            if not name:
                name = input(f"Current name: {user.name}\nNew name: ")
                if name:
                    user.name = name.lower()
                else:
                    raise ValueError("Name cannot be empty")
            if not password_changed:
                if password_counter != 0:
                    if input("Do you want to change the password? (y/n): ").lower() == "n": break
                    old_password = input(f"Enter your old password: ")
                    new_password = input(f"Enter your new password: ")

                    if user.change_password(new_password, old_password):
                        print("\nPassword changed successfully")
                        password_changed = True
                    else:
                        print(f"Old password must match and new password cannot be the same as the old, tries remaining: {password_counter}")
            else:
                exit_now = True
        except ValueError as error:
            print(error)

@line_split


# @line_split
# def save(data: dict):
#     success: bool
#     success = True
#
#     return success
@line_split
def load(db) -> dict:
    """load data from file"""
    data = db.load_data()
    data = \

    return data

def match_subject_name(name: str, data: dict) -> Subject | None:
    """match subject name to data"""
    for each in data["subjects"]:
        if each.name == name:
            return each
    return None

if __name__ == '__main__':
    main()
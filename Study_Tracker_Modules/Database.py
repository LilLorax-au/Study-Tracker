import sqlite3
from datetime import datetime

from Study_Tracker_Modules.User import User
from Study_Tracker_Modules.Subject import Subject
from Study_Tracker_Modules.Session import Session

class StudyTrackerDB:
    db_name = str("study_tracker.db")
    db_conn = sqlite3
    db_cursor = sqlite3

    # is the database start up method, creates a usable connection and curser that each other method can use
    def db_setup(self):
        try:
            # opening connection
            self.db_conn = sqlite3.connect(self.db_name)
            # cursor creation
            self.db_cursor = self.db_conn.cursor()
        except sqlite3.InternalError as error:
            print(f"Error: {error}")

    def build_schema(self):
        self.db_setup()
        query: list = ["CREATE TABLE IF NOT EXISTS user(id INTEGER PRIMARY KEY AUTOINCREMENT,"
                       " name TEXT,"
                       " password TEXT);",
                       "CREATE TABLE IF NOT EXISTS subjects(id INTEGER PRIMARY KEY AUTOINCREMENT,"
                       " name TEXT,"
                       " description TEXT,"
                       " goal INT,"
                       " difficulty INT);",
                       "CREATE TABLE IF NOT EXISTS sessions(session_id INTEGER PRIMARY KEY AUTOINCREMENT,"
                       " subject_name TEXT,"
                       " date TEXT,"
                       " session_time TEXT,"
                       " study_type TEXT,"
                       " subject_id INTEGER,"
                       " user_id INTEGER);",]
        try:
            for each in query:
                self.db_cursor.execute(each)
                self.db_conn.commit()
        except sqlite3.InternalError as error:
            print(f"Error: {error}")
        finally:
            self.db_conn.close()

    def rebuild_schema(self):
        self.db_setup()
        query: list = ["DROP TABLE IF EXISTS user;",
                       "DROP TABLE IF EXISTS subjects;",
                       "DROP TABLE IF EXISTS sessions;"]
        try:
            for each in query:
                self.db_cursor.execute(each)
                self.db_conn.commit()
        except sqlite3.InternalError as error:
            print(f"Error: {error}")
        finally:
            self.db_conn.close()
            self.build_schema()

    def save_data(self, data):
        self.rebuild_schema()
        self.db_setup()

        query_user: str = f"INSERT INTO user (id ,name, password) VALUES ({data["user"][0].user_id},'{data['user'][0].name}','{data['user'][0].password}');"
        query_subjects: str = f"INSERT INTO subjects(id, name, description, goal, difficulty) VALUES "
        query_sessions: str = f"INSERT INTO sessions(session_id, subject_name, date, session_time, study_type, subject_id, user_id) VALUES "

        for each in data["subjects"]:
            query_subjects += f"({each.subject_id},'{each.name}','{each.description}',{each.goal},{each.difficulty}),"
        query_subjects = query_subjects.strip(',') + ";"


        for each in data["sessions"]:
            query_sessions += f"({each.session_id}, '{each.subject_name}', '{each.date}', {each.session_time}, '{each.study_type}', '{each.subject_id}','{each.user_id}'),"
        query_sessions = query_sessions.strip(',') + ";"

        try:
            self.db_cursor.execute(query_user)
            self.db_conn.commit()
            self.db_cursor.execute(query_subjects)
            self.db_conn.commit()
            if len(data["sessions"]) > 0:
                self.db_cursor.execute(query_sessions)
                self.db_conn.commit()
        except sqlite3.InternalError as error:
            print(f"Error: {error}")
        finally:
            self.db_conn.close()

    def load_data(self) -> dict:
        self.db_setup()
        query_user: str = f"SELECT * FROM user;"
        query_subjects: str = f"SELECT * FROM subjects;"
        query_sessions: str = f"SELECT * FROM sessions;"
        data: dict = \
            {
                "user": [],
                "subjects": [],
                "sessions": []
            }

        self.db_cursor.execute(query_user)
        self.db_conn.commit()
        users = self.db_cursor.fetchall()

        self.db_cursor.execute(query_subjects)
        self.db_conn.commit()
        subjects = self.db_cursor.fetchall()

        self.db_cursor.execute(query_sessions)
        self.db_conn.commit()
        sessions = self.db_cursor.fetchall()

        for each in users:
            data["user"].append(User(int(each[0]), each[1], each[2]))
        for each in subjects:
            data["subjects"].append(Subject(int(each[0]), each[1], each[2], int(each[3]), int(each[4])))
        for each in sessions:
            data["sessions"].append(Session(int(each[0]), each[1], datetime.strptime(each[2], "%Y-%m-%d"), float(each[3]), each[4], int(each[5]), int(each[6])))

        return data



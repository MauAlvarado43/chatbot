import sqlite3
import json


class DB:

    def __init__(self):
        connection = sqlite3.connect('bot.db', check_same_thread=False)
        self.connection = connection
        self.init_database()
        self.init_data()

    def init_database(self):
        cursor = self.connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS botanswer (
                answer_id number auto_increment primary key, 
                answer text
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS keywords (
                word text,
                weight real,
                answer_id number,
                FOREIGN KEY(answer_id) REFERENCES botanswer(answer_id)
            )
        """)

    def init_data(self):

        with open('./fixtures.json', 'r', encoding='utf-8') as fixtures_file:
            fixtures = json.load(fixtures_file)

            cursor = self.connection.cursor()

            cursor.execute("DELETE FROM botanswer")
            cursor.execute("DELETE FROM keywords")

            for index, data in enumerate(fixtures):
                cursor.execute(f"INSERT INTO botanswer (answer, answer_id) VALUES ('{data['answer']}', {index})")
                if len(data['keywords']) != 0:
                    for index2, _ in enumerate(data['keywords']):
                        cursor.execute(f"INSERT INTO keywords (word, weight, answer_id) VALUES ('{data['keywords'][index2]}',{data['weights'][index2]}, {index})")

    def query(self, text):
        cursor = self.connection.cursor()
        data = cursor.execute(text)
        return data

    def get_all_answers(self):
        return self.query("SELECT answer_id, answer FROM botanswer")

    def get_all_keywords(self, answer_id):
        return self.query(f"SELECT answer_id, weight, word FROM keywords WHERE answer_id = {answer_id}")
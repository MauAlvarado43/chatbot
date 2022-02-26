import sqlite3


class DB:

    def __init__(self):
        connection = sqlite3.connect('bot.db')
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
                answer_id number
            )
        """)

    def init_data(self):

        fixtures = [
            {
                "answer": "Lo siento, no he podido entender lo que me dijiste",
                "keywords": [],
                "weights": []
            },
            {
                "answer": "Hola",
                "keywords": ["Hola", "que", "tal", "onda"],
                "weights": [1, 1, 1, 1]
            }
        ]

        cursor = self.connection.cursor()

        cursor.execute("DELETE FROM botanswer")
        cursor.execute("DELETE FROM keywords")

        for index, data in enumerate(fixtures):
            cursor.execute(f"INSERT INTO botanswer (answer, answer_id) VALUES ('{data['answer']}', {index})")
            if len(data['keywords']) != 0:
                for index2, _ in enumerate(fixtures):
                    cursor.execute(f"INSERT INTO keywords (word, weight, answer_id) VALUES ('{data['keywords'][index2]}',{data['weights'][index2]}, {index})")

    def query(self, text):
        cursor = self.connection.cursor()
        data = cursor.execute(text)
        return data


    def get_all_answers(self):
        return self.query("SELECT answer_id, answer FROM botanswer")

    def get_all_keywords(self, answer_id):
        return self.query(f"SELECT answer_id, weight, word FROM keywords WHERE answer_id = {answer_id}")
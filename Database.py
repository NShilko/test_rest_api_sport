import psycopg2
import os
from dotenv import load_dotenv


class MyDatabase:
    def __init__(self):
        # Загрузка переменных окружения
        load_dotenv('main.env')
        self.db_host = os.environ.get('FSTR_DB_HOST')
        self.db_port = os.environ.get('FSTR_DB_PORT')
        self.db_login = os.environ.get('FSTR_DB_LOGIN')
        self.db_password = os.environ.get('FSTR_DB_PASS')

        self.conn = psycopg2.connect(
            host=self.db_host,
            port=self.db_port,
            user=self.db_login,
            password=self.db_password,
            database='postgres'
        )

        if self.conn.status == psycopg2.extensions.STATUS_READY:
            print("Подключение к БД установлено!")
        else:
            print("Соединение с БД НЕ установлено!")

    def add_pereval(self, data):
        query = '''
            INSERT INTO pereval_added (
                user_email,
                beauty_title,
                title,
                other_titles,
                level_summer,
                level_autumn,
                level_winter,
                level_spring,
                connect,
                add_time,
                coord_id
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        '''
        with self.conn.cursor() as cur:
            cur.execute(query, (
                data['user_email'],
                data['beauty_title'],
                data['title'],
                data['other_titles'],
                data['level_summer'],
                data['level_autumn'],
                data['level_winter'],
                data['level_spring'],
                data['connect'],
                data['add_time'],
                data['coord_id']
            ))
            self.conn.commit()

    def close_connection(self):
        self.conn.close(())



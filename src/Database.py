import psycopg2
import os
from dotenv import load_dotenv
from fastapi import HTTPException
from src.Models import Pereval


class MyDatabase:
    def __init__(self):
        # Load environment variables from.env file
        load_dotenv('src/env/main.env')
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

        # check server status
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
            try:
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
                    data['coord_id'],
                ))

            except Exception as e:
                self.conn.rollback()
                return HTTPException(status_code=404, detail=f"Не удалось обновить запись: {e}")
            self.conn.commit()
            return {'state': 1, "message": "Данные успешно добавлены в базу данных"}

    def get_pereval_by_id(self, id: int):
        with self.conn.cursor() as cur:
            cur.execute("SELECT * FROM pereval_added WHERE id = %s", (id,))
            result = cur.fetchone()
            if result is None:
                return None
            columns = [desc[0] for desc in cur.description]
            return {columns[i]: result[i] for i in range(len(columns))}

    def get_user_perevals(self, email: str) -> list:
        with self.conn.cursor() as cur:
            cur.execute("SELECT * FROM pereval_added WHERE user_email=%s", (email,))
            rows = cur.fetchall()
            if rows:
                columns = [col[0] for col in cur.description]
                return [dict(zip(columns, row)) for row in rows]
            return None

    def update_pereval(self, id: int, data: dict) -> tuple:
        query = """
                UPDATE pereval_added 
                SET {} 
                WHERE id=%s AND status='new'
            """

        # get keys from fields and convert it for SET
        placeholders = ", ".join([f"{key}=%s" for key in data.keys()])
        # replace SET {} to SET keys
        query = query.format(placeholders)

        with self.conn:
            try:
                with self.conn.cursor() as cur:
                    cur.execute(query, (*data.values(), id))
                    return (1, "Запись успешно обновлена!")
            except Exception as e:
                self.conn.rollback()
                raise HTTPException(status_code=400, detail=f"Не удалось обновить запись: {e}")

    def close_connection(self):
        self.conn.close(())



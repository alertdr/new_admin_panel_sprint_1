import dataclasses
import os
import sqlite3

import psycopg2
from dotenv import load_dotenv
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor

from entities import Filmwork, Genre, Person, GenreFilmwork, PersonFilmwork

TABLES = ('film_work', 'genre', 'person', 'genre_film_work', 'person_film_work')
DATACLASSES = dict(zip(TABLES, (Filmwork, Genre, Person, GenreFilmwork, PersonFilmwork)))
# Load environments
load_dotenv()

dsl = {
    'dbname': os.environ.get('DB_NAME'),
    'user': os.environ.get('DB_USER'),
    'password': os.environ.get('DB_PASSWORD'),
    'host': os.environ.get('DB_HOST', '127.0.0.1'),
    'port': os.environ.get('DB_PORT', 5432)
}

sqlite_db_path = 'db.sqlite'


class SQLiteLoader:
    def __init__(self, connection):
        self.con = connection

    def load_movies(self) -> dict:
        data = {}
        cursor = self.con.cursor()
        for table in TABLES:
            film_work_columns = 'id, title, description, creation_date, rating, type, created_at, updated_at'
            columns = '*' if table != 'film_work' else film_work_columns
            cursor.execute('SELECT {0} FROM {1}'.format(columns, table))
            rows = cursor.fetchall()

            self._make_rows_pretty(rows, table, data)

        return data

    @staticmethod
    def _make_rows_pretty(rows: list, table: str, data: dict):
        dataclasses = []
        for row in rows:
            dataclasses.append(DATACLASSES[table](*row))

        data[table] = dataclasses


class PostgresSaver:
    def __init__(self, connection):
        self.con = connection

    def save_all_data(self, data: dict):
        cursor = self.con.cursor()
        for table in TABLES:
            columns = tuple(DATACLASSES[table].__annotations__.keys())
            columns_pretty = ', '.join(columns)
            mogrify_pattern = ', '.join(['%s'] * len(columns))
            args = ','.join(
                cursor.mogrify(f'({mogrify_pattern})', dataclasses.astuple(item)).decode() for item in data[table]
            )
            cursor.execute(f"""
                            INSERT INTO content.{table} ({columns_pretty})
                            VALUES {args}
                            ON CONFLICT (id) DO NOTHING
                            """)


def load_from_sqlite(connection: sqlite3.Connection, pg_conn: _connection):
    """Основной метод загрузки данных из SQLite в Postgres"""
    postgres_saver = PostgresSaver(pg_conn)
    sqlite_loader = SQLiteLoader(connection)

    data = sqlite_loader.load_movies()
    postgres_saver.save_all_data(data)


if __name__ == '__main__':
    psycopg2.extras.register_uuid()

    with sqlite3.connect(sqlite_db_path) as sqlite_conn, psycopg2.connect(**dsl, cursor_factory=DictCursor) as pg_conn:
        load_from_sqlite(sqlite_conn, pg_conn)

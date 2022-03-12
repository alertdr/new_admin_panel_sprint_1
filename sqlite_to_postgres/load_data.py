import dataclasses
import os
import sqlite3
from typing import Generator

import psycopg2
from attr import dataclass
from dotenv import load_dotenv
from entities import Filmwork, Genre, GenreFilmwork, Person, PersonFilmwork
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor

TABLES = {
    'film_work': Filmwork,
    'genre': Genre,
    'person': Person,
    'genre_film_work': GenreFilmwork,
    'person_film_work': PersonFilmwork
}
# Load environments
load_dotenv()

DSL = {
    'dbname': os.environ.get('DB_NAME'),
    'user': os.environ.get('DB_USER'),
    'password': os.environ.get('DB_PASSWORD'),
    'host': os.environ.get('DB_HOST', '127.0.0.1'),
    'port': os.environ.get('DB_PORT', 5432)
}

BATCH = 500
SQLITE_DB_PATH = 'db.sqlite'


class SQLiteLoader:
    def __init__(self, connection):
        self.con = connection

    def load_movies(self, table, model) -> Generator:
        cursor = self.con.cursor()
        cursor.execute('SELECT {0} FROM {1}'.format(model.sqlite_columns(), table))

        while rows := cursor.fetchmany(BATCH):
            yield self._make_rows_pretty(rows, model)

    @staticmethod
    def _make_rows_pretty(rows, model: dataclass):
        pretty_rows = []
        for row in rows:
            pretty_rows.append(model(*row))

        return pretty_rows


class PostgresSaver:
    def __init__(self, connection):
        self.con = connection

    def save_all_data(self, data: Generator, table, model):
        cursor = self.con.cursor()
        columns = tuple(model.__annotations__.keys())
        columns_pretty = ', '.join(columns)
        mogrify_pattern = ', '.join(['%s'] * len(columns))
        args = ','.join(
            cursor.mogrify(f'({mogrify_pattern})', dataclasses.astuple(item)).decode() for item in data
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
    for table, model in TABLES.items():
        data = sqlite_loader.load_movies(table, model)
        [postgres_saver.save_all_data(i, table, model) for i in data]


if __name__ == '__main__':
    psycopg2.extras.register_uuid()

    with sqlite3.connect(SQLITE_DB_PATH) as sqlite_conn, psycopg2.connect(**DSL, cursor_factory=DictCursor) as pg_conn:
        load_from_sqlite(sqlite_conn, pg_conn)

    sqlite_conn.close()
    pg_conn.close()

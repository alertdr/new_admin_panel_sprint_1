import sqlite3

import psycopg2
import pytest
from psycopg2.extras import DictCursor

from sqlite_to_postgres.load_data import TABLES, DATACLASSES, dsl


@pytest.fixture(scope='module')
def pg_conn():
    conn = psycopg2.connect(**dsl, cursor_factory=DictCursor)
    yield conn
    conn.close()


@pytest.fixture(scope='module')
def sqlite_conn():
    conn = sqlite3.connect('../../db.sqlite')
    yield conn
    conn.close()


def test_compare_len_tables(pg_conn, sqlite_conn):
    pg_cursor = pg_conn.cursor()
    sqlite_cursor = sqlite_conn.cursor()
    for table in TABLES:
        sqlite_table = get_sqlite_table(table, sqlite_cursor)
        pg_table = get_postgres_table(table, pg_cursor)

        assert len(sqlite_table) == len(pg_table)


def test_compare_all_rows(pg_conn, sqlite_conn):
    pg_cursor = pg_conn.cursor()
    sqlite_cursor = sqlite_conn.cursor()
    for table in TABLES:
        sqlite_table = get_sqlite_table(table, sqlite_cursor)
        pg_table = get_postgres_table(table, pg_cursor)

        for i in range(len(pg_table)):
            pg_row = DATACLASSES[table](**pg_table[i])
            sqlite_row = DATACLASSES[table](*sqlite_table[i])
            assert sqlite_row == pg_row


def get_sqlite_table(table: str, sqlite_cursor):
    film_work_columns = 'id, title, description, creation_date, rating, type, created_at, updated_at'
    columns = '*' if table != 'film_work' else film_work_columns

    sqlite_cursor.execute('SELECT {0} FROM {1} ORDER BY {2}'.format(columns, table, 'id'))

    return sqlite_cursor.fetchall()


def get_postgres_table(table: str, pg_cursor):
    pg_cursor.execute('SELECT * FROM {0} ORDER BY {1}'.format(table, 'id'))
    return pg_cursor.fetchall()

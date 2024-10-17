from collections import namedtuple
from dataclasses import dataclass
from functools import wraps
from typing import Optional

from mysql.connector.abstracts import MySQLConnectionAbstract, MySQLCursorAbstract
from mysql.connector.pooling import PooledMySQLConnection

@dataclass
class DatabaseMetadata:
    connection: PooledMySQLConnection | MySQLConnectionAbstract
    cursor: MySQLCursorAbstract


# Database objects
User = namedtuple("User", ["id", "name", "data"])


# Database helper methods
def get_user_data(cursor: MySQLCursorAbstract, username: str) -> Optional[User]:
    cursor.execute("select * from users where name = %s", (username,))
    result = cursor.fetchone()
    return User(*result) if result is not None else None


def get_all_users(cursor: MySQLCursorAbstract) -> list[User]:
    cursor.execute("select * from users")
    results = cursor.fetchall()
    return list(map(lambda r: User(*r), results))


def insert_user(cursor: MySQLCursorAbstract, username: str, data: str) -> None:
    cursor.execute("insert into users (name, data) values (%s, %s)", (username, data))


def update_user(cursor: MySQLCursorAbstract, username: str, data: str) -> None:
    cursor.execute("update users set data = %s where name = %s", (data, username))


def delete_user(cursor: MySQLCursorAbstract, username: str) -> None:
    cursor.execute("delete from users where name = %s", (username,))
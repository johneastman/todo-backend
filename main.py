from flask import Flask, Response, request, make_response
from dotenv import dotenv_values
from mysql import connector
from mysql.connector.abstracts import MySQLCursorAbstract, MySQLConnectionAbstract

import os
import json
from functools import wraps

from mysql.connector.pooling import PooledMySQLConnection

app = Flask(__name__)

ROOT_DIR = os.path.expanduser(app.root_path)

config = dotenv_values(os.path.join(ROOT_DIR, ".env"))


def db_conn(initialize=False):

    def actual_decorator(method):

        @wraps(method)
        def inner(*args, **kwargs):
            database_name = config.get("DB_NAME")

            if initialize:
                print(f"Database '{database_name}' does not exist. Creating.")
            else:
                print(f"Database '{database_name}' exists. Using.")

            base_conn_config = {
                "host": config.get("DB_HOST"),
                "user": config.get("DB_USER"),
                "password": config.get("DB_PASSWORD"),
            }

            # If the database is being initialized, it will not exist, so
            # the "database" field should not be included in the connection
            # configs. However, if the database does exist, include the
            # database in the configs so the endpoints can connect to it.
            conn_config = {
                **base_conn_config,
                **({} if initialize else {"database": database_name})
            }
            print(conn_config)

            with connector.connect(**conn_config) as connection:
                with connection.cursor(buffered=True) as cursor:
                    return method(connection, cursor, *args, **kwargs)
        return inner
    return actual_decorator


@db_conn(True)
def setup(
        connection: PooledMySQLConnection | MySQLConnectionAbstract,
        cursor: MySQLCursorAbstract):

    db_name = config.get("DB_NAME")

    cursor.execute(f"create database if not exists {db_name}")
    cursor.execute(f"use {db_name}")
    cursor.execute(
        "create table if not exists users(id int primary key auto_increment, name text not null, data text not null)")

# Initialize the database
setup()


@app.route("/users")
@db_conn()
def get_users(
        connection: PooledMySQLConnection | MySQLConnectionAbstract,
        cursor: MySQLCursorAbstract):

    cursor.execute("select name from users")
    results = cursor.fetchall()
    return make_response(list(map(lambda row: row[0], results)), 200)


@app.route("/users/<username>", methods=["GET", "POST", "DELETE"])
@db_conn()
def get_user(
        connection: PooledMySQLConnection | MySQLConnectionAbstract,
        cursor: MySQLCursorAbstract,
        username: str):

    if request.args.get("checkUserExists") == "true":

        cursor.execute(
            "select * from users where name = %s",
            (username,)
        )
        result = cursor.fetchone()

        body = {"username": username, "exists": result is not None}
        return make_response(body, 200)

    methods = {
        "GET": get,
        "POST": save,
        "DELETE": delete
    }

    return methods[request.method](connection, cursor, username)


@app.route("/config", methods=["GET"])
def get_config():
    return make_response(config, 200)


def get(
        connection: PooledMySQLConnection | MySQLConnectionAbstract,
        cursor: MySQLCursorAbstract,
        username: str) -> Response:

    try:
        cursor.execute(
            "select data from users where name = %s",
            (username,)
        )
        result = cursor.fetchone()

        if result is None:
            return make_response({"message": "User does not exist"}, 404)

        body = json.loads(result[0])
        return make_response(body, 200)
    except Exception as e:
        print(e)
        return make_response({"message": "Unable to retrieve user data"}, 500)


def save(connection: PooledMySQLConnection | MySQLConnectionAbstract, cursor: MySQLCursorAbstract, username: str) -> Response:
    try:
        user_data = json.dumps(request.json)

        cursor.execute("select * from users where name = %s", (username,))
        result = cursor.fetchone()
        if result is not None:
            # Update data if a row already exists
            print(f"Updating data for {username}")
            cursor.execute("update users set data = %s where name = %s", (user_data, username))
        else:
            # Insert new row if the row does not exist
            print(f"Creating data for {username}")
            cursor.execute("insert into users (name, data) values (%s, %s)", (username, user_data))

        connection.commit()

        return make_response({"message": "Data saved successfully"}, 200)
    except Exception as e:
        print(e)
        return make_response({"message": "Failed to save user data"}, 500)


def delete(
        connection: PooledMySQLConnection | MySQLConnectionAbstract,
        cursor: MySQLCursorAbstract,
        username: str) -> Response:

    try:
        # Check if the user exists.
        cursor.execute("select * from users where name = %s", (username,))
        result = cursor.fetchone()
        if result is None:
            return make_response({"message": "User not found"}, 404)

        # If the user does exist, delete their row from the database.
        cursor.execute("delete from users where name = %s", (username,))

        connection.commit()

        return make_response({"message": "Data successfully deleted"}, 200)

    except Exception as e:
        print(e)
        return make_response({"message": "Failed to delete data"}, 404)


if __name__ == "__main__":
    app.run()

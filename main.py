from flask import Flask, Response, request, make_response
from dotenv import dotenv_values
from mysql import connector

import os
import json

app = Flask(__name__)

ROOT_DIR = os.path.expanduser(app.root_path)

config = dotenv_values(os.path.join(ROOT_DIR, ".env"))
print("Environment data", config)


# Database Setup
def connect_to_db(name):
    """Initiates a connection to the database

    :param name: name of the database
    :type name: str
    :return: database object and cursor
    :rtype: (PooledMySQLConnection | MySQLConnectionAbstract,  MySQLCursorAbstract)
    """
    db = connector.connect(
        host=config.get("DB_HOST"),
        user=config.get("DB_USER"),
        password=config.get("DB_PASSWORD"),
        database=name
    )
    return db, db.cursor(buffered=True)


db_name = config.get("DB_NAME")
setup_db, setup_cursor = connect_to_db(db_name)

setup_cursor.execute(f"create database if not exists {db_name}")
setup_cursor.execute(f"use {db_name}")
setup_cursor.execute(
    "create table if not exists users(id int primary key auto_increment, name text not null, data text not null)")

setup_cursor.close()
setup_db.disconnect()


@app.route("/users")
def get_users():
    get_users_db, get_users_cursor = connect_to_db(db_name)
    get_users_cursor.execute("select name from users")
    results = get_users_cursor.fetchall()

    get_users_cursor.close()
    get_users_db.disconnect()

    return make_response(list(map(lambda row: row[0], results)), 200)


@app.route("/users/<username>", methods=["GET", "POST", "DELETE"])
def get_user(username):
    if request.args.get("checkUserExists") == "true":

        get_user_db, get_user_cursor = connect_to_db(db_name)
        get_user_cursor.execute(
            "select * from users where name = %s",
            (username,)
        )
        result = get_user_cursor.fetchone()

        get_user_cursor.close()
        get_user_db.disconnect()

        body = {"username": username, "exists": result is not None}
        return make_response(body, 200)

    methods = {
        "GET": get,
        "POST": save,
        "DELETE": delete
    }

    return methods[request.method](username)


@app.route("/config", methods=["GET"])
def get_config():
    return make_response(config, 200)


def get(username: str) -> Response:
    try:
        get_db, get_cursor = connect_to_db(db_name)
        get_cursor.execute(
            "select data from users where name = %s",
            (username,)
        )
        result = get_cursor.fetchone()

        get_cursor.close()
        get_db.disconnect()

        if result is None:
            return make_response({"message": "User does not exist"}, 404)

        body = json.loads(result[0])
        return make_response(body, 200)
    except Exception as e:
        print(e)
        return make_response({"message": "Internal Server Error"}, 500)


def save(username: str) -> Response:
    try:
        user_data = json.dumps(request.json)

        save_db, save_cursor = connect_to_db(db_name)

        save_cursor.execute("select * from users where name = %s", (username,))
        result = save_cursor.fetchone()
        if result is not None:
            # Update data if a row already exists
            print(f"Updating data for {username}")
            save_cursor.execute("update users set data = %s where name = %s", (user_data, username))
        else:
            # Insert new row if the row does not exist
            print(f"Creating data for {username}")
            save_cursor.execute("insert into users (name, data) values (%s, %s)", (username, user_data))

        save_db.commit()

        save_cursor.close()
        save_db.disconnect()

        return make_response({"message": "Data saved successfully"}, 200)
    except Exception as e:
        print(e)
        return make_response({"message": "Failed to save user data"}, 500)


def delete(username: str) -> Response:
    try:
        delete_db, delete_cursor = connect_to_db(db_name)

        # Check if the user exists.
        delete_cursor.execute("select * from users where name = %s", (username,))
        result = delete_cursor.fetchone()
        if result is None:
            return make_response({"message": "User not found"}, 404)

        # If the user does exist, delete their row from the database.
        delete_cursor.execute("delete from users where name = %s", (username,))

        delete_db.commit()

        delete_cursor.close()
        delete_db.disconnect()

        return make_response({"message": "Data successfully deleted"}, 200)

    except Exception as e:
        print(e)
        return make_response({"message": "Failed to delete data"}, 404)


if __name__ == "__main__":
    app.run()

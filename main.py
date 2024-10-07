from flask import Flask, Response, request, make_response
from dotenv import dotenv_values
from mysql import connector

import os
import json

app = Flask(__name__)

ROOT_DIR = os.path.expanduser(app.root_path)

config = dotenv_values(os.path.join(ROOT_DIR, ".env"))
print(config)

db = connector.connect(
  host=config.get("DB_HOST"),
  user=config.get("DB_USER"),
  password=config.get("DB_PASSWORD")
)

setup_cursor = db.cursor()

db_name = config.get("DB_NAME")
setup_cursor.execute(f"create database if not exists {db_name}")
setup_cursor.execute(f"use {db_name}")
setup_cursor.execute(
    "create table if not exists users(id int primary key auto_increment, name text not null, data text not null)")
setup_cursor.close()


@app.route("/users")
def get_users():
    all_users_cursor = db.cursor(buffered=True)
    all_users_cursor.execute("select name from users")
    results = all_users_cursor.fetchall()
    all_users_cursor.close()

    return make_response(list(map(lambda row: row[0], results)), 200)


@app.route("/users/<username>", methods=["GET", "POST", "DELETE"])
def get_user(username):
    if request.args.get("checkUserExists") == "true":
        user_cursor = db.cursor(buffered=True)
        user_cursor.execute(
            "select * from users where name = %s",
            (username,)
        )
        result = user_cursor.fetchone()
        user_cursor.close()

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
    user_cursor = db.cursor(buffered=True)
    user_cursor.execute(
        "select data from users where name = %s",
        (username,)
    )
    result = user_cursor.fetchone()
    user_cursor.close()

    if result is None:
        return make_response({"message": "User does not exist"}, 404)

    body = json.loads(result[0])
    return make_response(body, 200)


def save(username: str) -> Response:
    try:
        user_data = json.dumps(request.json)

        update_cursor = db.cursor(buffered=True)

        update_cursor.execute("select * from users where name = %s", (username,))
        result = update_cursor.fetchone()
        if result is not None:
            # Update data if a row already exists
            print(f"Updating data for {username}")
            update_cursor.execute("update users set data = %s where name = %s", (user_data, username))
        else:
            # Insert new row if the row does not exist
            print(f"Creating data for {username}")
            update_cursor.execute("insert into users (name, data) values (%s, %s)", (username, user_data))

        db.commit()

        return make_response({"message": "Data saved successfully"}, 200)
    except Exception as e:
        return make_response({"message": str(e)}, 500)


def delete(username: str) -> Response:
    try:
        delete_cursor = db.cursor(buffered=True)

        # Check if the user exists.
        delete_cursor.execute("select * from users where name = %s", (username,))
        result = delete_cursor.fetchone()
        if result is None:
            return make_response({"message": "User not found"}, 404)

        # If the user does exist, delete their row from the database.
        delete_cursor.execute("delete from users where name = %s", (username,))
        db.commit()

        return make_response({"message": "Data successfully deleted"}, 200)
    except Exception as e:
        return make_response({"message": "Failed to "}, 404)


if __name__ == "__main__":
    app.run()

from flask import Flask, Response, request, make_response
import os
import json

app = Flask(__name__)


@app.route("/users")
def get_users():
    user_data = list(
        map(
            lambda filename: filename.split(".")[0],
            filter(
                lambda filename: filename.endswith("json"),
                os.listdir())))
    print(user_data)
    return make_response(user_data, 200)


@app.route("/users/<username>", methods=["GET", "POST", "DELETE"])
def get_user(username):
    project_folder = os.path.expanduser(app.root_path)
    file_path = os.path.join(project_folder, f"{username}.json")

    if request.args.get("checkUserExists") == "true":
        body = {username: os.path.isfile(file_path)}
        return make_response(body, 200)

    methods = {
        "GET": get,
        "POST": save,
        "DELETE": delete
    }

    return methods[request.method](file_path)


def get(file_path: str) -> Response:
    try:
        with open(file_path, "r") as file:
            file_content = file.read()
            body = json.loads(file_content)
            return make_response(body, 200)
    except FileNotFoundError:
        return make_response({"message": "File not found"}, 404)


def save(file_path: str) -> Response:
    try:
        with open(file_path, "w") as file:
            file_content = json.dumps(request.json)
            file.write(file_content)
            return make_response({"message": "Data saved successfully"}, 200)
    except Exception as e:
        return make_response({"message": str(e)}, 500)


def delete(file_path: str) -> Response:
    try:
        os.remove(file_path)
        return make_response({"message": "Data successfully deleted"}, 200)
    except FileNotFoundError:
        return make_response({"message": "File not found"}, 404)


if __name__ == "__main__":
    app.run()

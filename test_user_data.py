from main import app

import json
import pytest


@pytest.fixture()
def application():
    app.config.update({
        "TESTING": True,
    })

    # other setup can go here

    yield app

    # clean up / reset resources here


@pytest.fixture()
def client(application):
    return app.test_client()


@pytest.fixture()
def runner(application):
    return app.test_cli_runner()


def test_save_user_data(client):
    response = client.post("/users/test", json={
        "listsJSON": [
            {
                "name": "A",
                "listType": "List",
                "defaultNewItemPosition": "bottom",
                "isSelected": "false",
                "items": [
                    {
                        "name": "1",
                        "notes": "this note is very important.",
                        "quantity": 1,
                        "isComplete": "false",
                        "isSelected": "false",
                        "isLocked": "true"
                    },
                    {
                        "name": "2",
                        "notes": "",
                        "quantity": 1,
                        "isComplete": "false",
                        "isSelected": "false",
                        "isLocked": "false"
                    },
                    {
                        "name": "3",
                        "notes": "",
                        "quantity": 1,
                        "isComplete": "false",
                        "isSelected": "false",
                        "isLocked": "false"
                    },
                    {
                        "name": "4",
                        "notes": "",
                        "quantity": 1,
                        "isComplete": "false",
                        "isSelected": "false",
                        "isLocked": "false"
                    },
                    {
                          "name": "5",
                          "notes": "",
                          "quantity": 1,
                          "isComplete": "false",
                          "isSelected": "false",
                          "isLocked": "false"
                    }
                ],
                "isLocked": "false"
            },
            {
                "name": "B",
                "listType": "Shopping",
                "defaultNewItemPosition": "bottom",
                "isSelected": "false",
                "items": [
                    {
                        "name": "Groceries",
                        "notes": "we need food. we're very hungry. but we are also very POOR!\n\nnew line!",
                        "quantity": 3,
                        "isComplete": "false",
                        "isSelected": "false",
                        "isLocked": "false"
                    }
                ],
                "isLocked": "false"
            },
            {
                "name": "C",
                "listType": "To-Do",
                "defaultNewItemPosition": "bottom",
                "isSelected": "false",
                "items": [
                    {
                        "name": "10",
                        "notes": "",
                        "quantity": 1,
                        "isComplete": "false",
                        "isSelected": "false",
                        "isLocked": "false"
                    },
                    {
                        "name": "12",
                        "notes": "",
                        "quantity": 1,
                        "isComplete": "false",
                        "isSelected": "false",
                        "isLocked": "false"
                    },
                    {
                        "name": "14",
                        "notes": "",
                        "quantity": 1,
                        "isComplete": "false",
                        "isSelected": "false",
                        "isLocked": "true"
                    },
                    {
                        "name": "16",
                        "notes": "",
                        "quantity": 1,
                        "isComplete": "false",
                        "isSelected": "false",
                        "isLocked": "false"
                    }
                ],
                "isLocked": "false"
            },
            {
                "name": "D",
                "listType": "Ordered To-Do",
                "defaultNewItemPosition": "bottom",
                "isSelected": "false",
                "items": [],
                "isLocked": "false"
            }
        ],
        "settingsJSON": {
            "isDeveloperModeEnabled": "false",
            "defaultListPosition": "bottom",
            "defaultListType": "List"
          }
    })

    assert response.status_code == 200

    body = json.loads(response.data)
    assert body["message"] == "Data saved successfully"


def test_check_if_user_exists(client):
    response = client.get("/users/test", query_string={"checkUserExists": "true"})
    assert response.status_code == 200

    body = json.loads(response.data)
    assert body["username"] == "test"
    assert body["exists"] == True


def test_get_all_users(client):
    response = client.get("/users")
    assert response.status_code == 200

    body = json.loads(response.data)
    assert body == ["test"]


def test_get_user_data(client):
    response = client.get("/users/test")
    assert response.status_code == 200

    body = json.loads(response.data)
    assert body["listsJSON"] is not None
    assert body["settingsJSON"] is not None


def test_check_if_user_does_not_exists(client):
    response = client.get("/users/invalidUser", query_string={"checkUserExists": "true"})
    assert response.status_code == 200

    body = json.loads(response.data)
    assert body["username"] == "invalidUser"
    assert body["exists"] == False


def test_get_user_data_that_does_not_exist(client):
    response = client.get("/users/invalidUser")
    assert response.status_code == 404

    body = json.loads(response.data)
    assert body["message"] == "User does not exist"


def test_save_user_data_invalid_json(client):
    response = client.post("/users/test", data='{', content_type='application/json')

    assert response.status_code == 500

    body = json.loads(response.data)
    assert body["message"] == "Failed to save user data"


def test_save_user_data_invalid_media_type(client):
    response = client.post("/users/test", data='abc')

    assert response.status_code == 500

    body = json.loads(response.data)
    assert body["message"] == "Failed to save user data"


def test_delete_user_data(client):
    response = client.delete("/users/test")

    assert response.status_code == 200

    body = json.loads(response.data)
    assert body["message"] == "Data successfully deleted"


def test_delete_user_data_does_not_exist(client):
    response = client.delete("/users/invalidUser")

    assert response.status_code == 404

    body = json.loads(response.data)
    assert body["message"] == "User not found"

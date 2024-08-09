import pytest
import json
from main import app


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


def test_check_if_user_exists_when_user_exists(client):
    response = client.get("/lists/test", query_string={"checkUserExists": "true"})
    assert response.status_code == 200

    body = json.loads(response.data)
    assert body["test"] == "true"


def test_check_if_user_exists_when_user_does_not_exists(client):
    response = client.get("/lists/invalidUser", query_string={"checkUserExists": "true"})
    assert response.status_code == 200

    body = json.loads(response.data)
    assert body["invalidUser"] == "false"

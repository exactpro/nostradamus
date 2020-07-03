import requests


REGISTER_URL = "auth/register/"


def test_get_teams(sql_conn, host):
    request = requests.get(host + REGISTER_URL)
    teams = {team["name"] for team in request.json()}

    sql_conn.execute("SELECT name FROM authentication_team")
    db_teams = set(*sql_conn.fetchall())

    assert db_teams == teams


def test_register_result(host, test_user):
    request = requests.post(host + REGISTER_URL, params=test_user)
    assert request.json() == {"result": "success"}


def test_register_error(host, test_user):
    request = requests.post(host + REGISTER_URL, params=test_user)

    assert request.status_code == 500


def test_registered_user(sql_conn, test_user):
    sql_conn.execute(
        "SELECT * FROM authentication_user WHERE name=(?) AND email=(?)",
        (test_user["name"], test_user["email"]),
    )

    result = sql_conn.fetchall()

    assert result is not None


def test_password_length(host):
    payload = {
        "team": 1,
        "name": "test_user2",
        "email": "test_user2@test.com",
        "password": 1234,
    }

    request = requests.post(host + REGISTER_URL, params=payload)

    assert (
        request.status_code == 500
        and request.json()["exception"]["fields"][0]["name"] == "password"
    )


def test_whitespaces_credentials(host):
    payload = {
        "team": 1,
        "name": "test_user 3",
        "email": "test_user3@test.com",
        "password": 123456,
    }

    request = requests.post(host + REGISTER_URL, params=payload)

    assert request.json()["exception"]["fields"][0]["name"] == "name"

import requests


SIGN_IN_URL = "auth/signin/"


def test_auth_by_username(host, test_user):
    payload = {
        "credentials": test_user["name"],
        "password": test_user["password"],
    }

    request = requests.post(host + SIGN_IN_URL, params=payload)
    data = request.json()

    assert data is not None and "exception" not in data


def test_auth_by_email(host, test_user):
    payload = {
        "credentials": test_user["email"],
        "password": test_user["password"],
    }

    request = requests.post(host + SIGN_IN_URL, params=payload)
    data = request.json()

    assert data is not None and "exception" not in data


def test_auth_error(host, test_user):
    payload = {"credentials": test_user["email"], "password": "1234Pass"}

    request = requests.post(host + SIGN_IN_URL, params=payload)
    data = request.json()

    assert data is not None and "exception" in data


def test_auth_data(sql_conn, host, test_user):
    payload = {
        "credentials": test_user["email"],
        "password": test_user["password"],
    }

    team = sql_conn.execute(
        "SELECT name FROM authentication_team WHERE id = (?)",
        (test_user["team"],),
    ).fetchone()[0]

    user_id = sql_conn.execute(
        "SELECT id FROM authentication_user WHERE email = (?)",
        (test_user["email"],),
    ).fetchone()[0]

    role = sql_conn.execute(
        """
        SELECT
            name
        FROM
            authentication_role AS r
            INNER JOIN
                authentication_teammember AS tm
            ON r.id = tm.role_id
        WHERE
            tm.user_id = (?)
        """,
        (user_id,),
    ).fetchone()[0]

    request = requests.post(host + SIGN_IN_URL, params=payload)
    data = request.json()

    assert (
        data["id"] == user_id
        and data["name"] == test_user["name"]
        and data["email"] == test_user["email"]
        and data["team"] == team
        and data["role"] == role
    )


def test_auth_token(host, test_user):
    payload = {
        "credentials": test_user["email"],
        "password": test_user["password"],
    }

    filter_route = "analysis_and_training/filter/"

    request = requests.post(host + SIGN_IN_URL, params=payload)
    token = "JWT " + request.json()["token"]
    headers = {"Authorization": token}

    request = requests.get(host + filter_route, headers=headers)

    assert request.status_code == 200

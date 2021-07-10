import pytest

from string import ascii_lowercase
from random import choice

from models.User import User


@pytest.fixture(scope="class")
def host(request):
    host = "http://localhost:8080/"
    request.cls.host = host


@pytest.fixture(scope="class")
def register_url(request):
    request.cls.register_url = "register/"


@pytest.fixture(scope="class")
def signin_url(request):
    request.cls.signin_url = "sign_in/"


@pytest.fixture(scope="class")
def verify_token_url(request):
    request.cls.verify_token_url = "verify_token/"


@pytest.fixture(scope="class")
def test_user_1(request):
    request.cls.test_user_1 = {
        "name": "".join(choice(ascii_lowercase) for _ in range(20)),
        "email": f"{''.join(choice(ascii_lowercase) for _ in range(20))}@test.com",
        "password": 123456,
    }


@pytest.fixture(scope="class")
def test_user_2(request):
    request.cls.test_user_2 = {
        "name": "".join(choice(ascii_lowercase) for _ in range(20)),
        "email": f"{''.join(choice(ascii_lowercase) for _ in range(20))}@test.com",
        "password": 123456,
    }

@pytest.fixture(scope="class")
def test_user_model(request):
    request.cls.test_user_model = User(id=100500, email="test@gmail.com", name="test", password="123456")

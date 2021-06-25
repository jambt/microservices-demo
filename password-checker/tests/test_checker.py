import pytest
from fastapi.testclient import TestClient
import main


@pytest.fixture
def client():
    client = TestClient(main.app)
    return client


def test_password_curl(client):
    response = client.post("/check-password", json={"password": "password"})
    assert response.status_code == 200
    assert '{"name":"Number of characters","count":8,"bonus":32,"type":"Addition"}' in response.content.decode('utf-8')


def test_password_method(client):
    response = client.get("/check-password")
    assert response.status_code == 405
    assert response.content == '{"detail":"Method Not Allowed"}'.encode('utf-8')


def test_length_check():
    result = main.length_check("!tAeBsCt123@")
    assert ({
        "name": "Number of characters",
        "count": 12,
        "bonus": 48,
        "type": "Addition"
            } == result)


def test_middle_numbers_or_symbols():
    result = main.middle_numbers_or_symbols('1aA9!zz@')
    assert ({
        "name": "Middle numbers or symbols",
        "count": 2,
        "bonus": 12,
        "type": "Addition"
            } == result)


def test_repeated_characters():
    result = main.repeat_characters('AbCdAdCbFf')
    assert({
        "name": "Repeated Characters",
        "count": 8,
        "bonus": -12,
        "type": "Deduction"
    } == result)

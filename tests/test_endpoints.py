import pytest
from fastapi.testclient import TestClient

from main import app


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


def test_create_person(client: TestClient):
    person = {
        "apelido": "josé",
        "nome": "José Roberto",
        "nascimento": "2000-10-01",
        "stack": ["C#", "Node", "Oracle"],
    }
    response = client.post("/pessoas", json=person)
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


def test_get_person(client: TestClient):
    response = client.get("/pessoas")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


def test_get_persons_by_term(client: TestClient):
    response = client.get("/pessoas")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


def test_count_persons(client: TestClient):
    response = client.get("/pessoas")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

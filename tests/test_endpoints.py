import re
from uuid import UUID

import pytest
from fastapi.testclient import TestClient

from main import app

RE_PERSON_URL = re.compile(
    r"^/pessoas/[\d\w]{8}-[\d\w]{4}-[\d\w]{4}-[\d\w]{4}-[\d\w]{12}"
)


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


def test_create_person(client: TestClient):
    persons = [
        {
            "apelido": "josé",
            "nome": "José Roberto",
            "nascimento": "2000-10-01",
            "stack": ["C#", "Node", "Oracle"],
        },
        {
            "apelido": "ana",
            "nome": "Ana Barbosa",
            "nascimento": "1985-09-23",
            "stack": None,
        },
    ]
    for person in persons:
        response = client.post("/pessoas", json=person)
        assert response.status_code == 201
        location = response.headers["Location"]
        assert RE_PERSON_URL.match(location) is not None


def test_create_person_duplicated_person(client: TestClient):
    # caso "josé" já tenha sido criado em outra requisição
    person = {
        "apelido": "josé",
        "nome": "José Roberto",
        "nascimento": "2000-10-01",
        "stack": ["C#", "Node", "Oracle"],
    }

    response = client.post("/pessoas", json=person)
    assert response.status_code == 201
    location = response.headers["Location"]
    assert RE_PERSON_URL.match(location) is not None

    response = client.post("/pessoas", json=person)
    assert response.status_code == 422


def test_create_person_empty_fields(client: TestClient):
    persons = [
        {
            "apelido": "ana",
            "nome": None,  # não pode ser None
            "nascimento": "1985-09-23",
            "stack": None,
        },
        {
            "apelido": None,  # não pode ser None
            "nome": "Ana Barbosa",
            "nascimento": "1985-01-23",
            "stack": None,
        },
    ]
    for person in persons:
        response = client.post("/pessoas", json=person)
        assert response.status_code == 422


def test_create_person_invalid_payload(client: TestClient):
    persons = [
        {
            "apelido": "apelido",
            "nome": 1,  # nome deve ser string e não número
            "nascimento": "1985-01-01",
            "stack": None,
        },
        {
            "apelido": "apelido",
            "nome": "nome",
            "nascimento": "1985-01-01",
            "stack": [1, "PHP"],  # stack deve ser um array de apenas strings
        },
    ]
    for person in persons:
        response = client.post("/pessoas", json=person)
        assert response.status_code == 400


def test_get_person_detail(client: TestClient):
    person = {
        "apelido": "josé",
        "nome": "José Roberto",
        "nascimento": "2000-10-01",
        "stack": ["C#", "Node", "Oracle"],
    }
    response_create = client.post("/pessoas", json=person)
    assert response_create.status_code == 201

    response_detail = client.get(response_create.headers["Location"])
    assert response_detail.status_code == 200

    payload = response_detail.json()

    assert is_valid_uuid(payload["apelido"])
    assert payload["id"] == person["apelido"]
    assert payload["nome"] == person["nome"]
    assert payload["nascimento"] == person["nascimento"]
    assert payload["stack"] == person["stack"]


def test_get_person_detail_not_found(client: TestClient):
    response = client.get("/pessoas/65945492-427b-4d31-9793-c3bcdb43d6f1")
    assert response.status_code == 404


def test_get_persons_by_term_01(client: TestClient):
    persons = [
        {
            "id": "f7379ae8-8f9b-4cd5-8221-51efe19e721b",
            "apelido": "josé",
            "nome": "José Roberto",
            "nascimento": "2000-10-01",
            "stack": ["C#", "Node", "Oracle"],
        },
        {
            "id": "5ce4668c-4710-4cfb-ae5f-38988d6d49cb",
            "apelido": "ana",
            "nome": "Ana Barbosa",
            "nascimento": "1985-09-23",
            "stack": ["Node", "Postgres"],
        },
    ]

    for person in persons:
        response = client.post("/pessoas", json=person)
        assert response.status_code == 422

    response = client.get("/pessoas", params={"t": "node"})
    assert response.status_code == 200
    payload = response.json()
    assert len(payload) == 2
    assert payload[0] == person[0]
    assert payload[1] == person[1]


def test_get_persons_by_term_02(client: TestClient):
    persons = [
        {
            "id": "f7379ae8-8f9b-4cd5-8221-51efe19e721b",
            "apelido": "josé",
            "nome": "José Roberto",
            "nascimento": "2000-10-01",
            "stack": ["C#", "Node", "Oracle"],
        },
        {
            "id": "5ce4668c-4710-4cfb-ae5f-38988d6d49cb",
            "apelido": "ana",
            "nome": "Ana Barbosa",
            "nascimento": "1985-09-23",
            "stack": ["Node", "Postgres"],
        },
    ]

    for person in persons:
        response = client.post("/pessoas", json=person)
        assert response.status_code == 422

    response = client.get("/pessoas", params={"t": "berto"})
    assert response.status_code == 200
    payload = response.json()
    assert len(payload) == 1
    assert payload[0] == person[0]


def test_get_persons_by_term_not_in_db(client: TestClient):
    persons = [
        {
            "id": "f7379ae8-8f9b-4cd5-8221-51efe19e721b",
            "apelido": "josé",
            "nome": "José Roberto",
            "nascimento": "2000-10-01",
            "stack": ["C#", "Node", "Oracle"],
        },
        {
            "id": "5ce4668c-4710-4cfb-ae5f-38988d6d49cb",
            "apelido": "ana",
            "nome": "Ana Barbosa",
            "nascimento": "1985-09-23",
            "stack": ["Node", "Postgres"],
        },
    ]

    for person in persons:
        response = client.post("/pessoas", json=person)
        assert response.status_code == 422

    response = client.get("/pessoas", params={"t": "Python"})
    assert response.status_code == 200
    payload = response.json()
    assert len(payload) == 0


def test_get_persons_by_term_empty(client: TestClient):
    response = client.get("/pessoas")
    assert response.status_code == 400


def test_count_persons(client: TestClient):
    response = client.get("/contagem-pessoas")
    assert response.status_code == 200
    assert response.body.isnumeric()


def is_valid_uuid(uuid_to_test):
    try:
        uuid_obj = UUID(uuid_to_test, version=4)
    except ValueError:
        return False
    return str(uuid_obj) == uuid_to_test

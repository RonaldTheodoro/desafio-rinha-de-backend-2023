import re


RE_PERSON_URL = re.compile(
    r"^/pessoas/[\d\w]{8}-[\d\w]{4}-[\d\w]{4}-[\d\w]{4}-[\d\w]{12}"
)


def test_create_person(client):
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


def test_create_person_duplicated_person(client):
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


def test_create_person_empty_fields(client):
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


def test_create_person_invalid_payload(client):
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

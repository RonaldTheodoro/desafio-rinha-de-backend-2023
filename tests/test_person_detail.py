from uuid import UUID


def test_get_person_detail(client):
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


def test_get_person_detail_not_found(client):
    response = client.get("/pessoas/65945492-427b-4d31-9793-c3bcdb43d6f1")
    assert response.status_code == 404


def is_valid_uuid(uuid_to_test):
    try:
        uuid_obj = UUID(uuid_to_test, version=4)
    except ValueError:
        return False
    return str(uuid_obj) == uuid_to_test

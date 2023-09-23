def test_get_persons_by_term_01(client):
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


def test_get_persons_by_term_02(client):
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


def test_get_persons_by_term_not_in_db(client):
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


def test_get_persons_by_term_empty(client):
    response = client.get("/pessoas")
    assert response.status_code == 400

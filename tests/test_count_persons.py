def test_count_persons(client):
    response = client.get("/contagem-pessoas")
    assert response.status_code == 200
    assert response.body.isnumeric()

def test_create_and_list_notes(client):
    payload = {"title": "Test", "content": "Hello world"}
    r = client.post("/notes/", json=payload)
    assert r.status_code == 201, r.text
    data = r.json()
    assert data["title"] == "Test"

    r = client.get("/notes/")
    assert r.status_code == 200
    body = r.json()
    assert "items" in body
    assert "total" in body
    assert body["total"] >= 1
    assert len(body["items"]) >= 1

    r = client.get("/notes/search/")
    assert r.status_code == 200

    r = client.get("/notes/search/", params={"q": "Hello"})
    assert r.status_code == 200
    items = r.json()
    assert len(items) >= 1


def test_notes_pagination(client):
    # Seed 3 notes
    for i in range(3):
        client.post("/notes/", json={"title": f"Note {i}", "content": f"Content {i}"})

    # Page 1 with page_size=2
    r = client.get("/notes/", params={"page": 1, "page_size": 2})
    assert r.status_code == 200
    body = r.json()
    assert body["total"] == 3
    assert len(body["items"]) == 2

    # Page 2 with page_size=2 (last page, 1 item)
    r = client.get("/notes/", params={"page": 2, "page_size": 2})
    assert r.status_code == 200
    body = r.json()
    assert body["total"] == 3
    assert len(body["items"]) == 1

    # Empty last page
    r = client.get("/notes/", params={"page": 3, "page_size": 2})
    assert r.status_code == 200
    body = r.json()
    assert body["total"] == 3
    assert len(body["items"]) == 0


def test_notes_pagination_invalid_params(client):
    # page < 1
    r = client.get("/notes/", params={"page": 0})
    assert r.status_code == 422

    # page_size < 1
    r = client.get("/notes/", params={"page_size": 0})
    assert r.status_code == 422

    # page_size > 100
    r = client.get("/notes/", params={"page_size": 101})
    assert r.status_code == 422

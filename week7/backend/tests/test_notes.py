def test_create_list_and_patch_notes(client):
    payload = {"title": "Test", "content": "Hello world"}
    r = client.post("/notes/", json=payload)
    assert r.status_code == 201, r.text
    data = r.json()
    assert data["title"] == "Test"
    assert "created_at" in data and "updated_at" in data

    r = client.get("/notes/")
    assert r.status_code == 200
    items = r.json()
    assert len(items) >= 1

    r = client.get("/notes/", params={"q": "Hello", "limit": 10, "sort": "-created_at"})
    assert r.status_code == 200
    items = r.json()
    assert len(items) >= 1

    note_id = data["id"]
    r = client.patch(f"/notes/{note_id}", json={"title": "Updated"})
    assert r.status_code == 200
    patched = r.json()
    assert patched["title"] == "Updated"


def test_pagination(client):
    """Verify that skip and limit query params control the returned page."""
    # Create 7 notes
    for i in range(7):
        client.post("/notes/", json={"title": f"Note {i}", "content": f"Content {i}"})

    # First page: limit=5, skip=0 -> should return 5 notes
    r = client.get("/notes/", params={"limit": 5, "skip": 0})
    assert r.status_code == 200
    items = r.json()
    assert len(items) == 5

    # Second page: limit=5, skip=5 -> should return remaining 2 notes
    r = client.get("/notes/", params={"limit": 5, "skip": 5})
    assert r.status_code == 200
    items = r.json()
    assert len(items) == 2


def test_sorting(client):
    """Verify ascending and descending sort by title."""
    client.post("/notes/", json={"title": "Banana", "content": "b"})
    client.post("/notes/", json={"title": "Apple", "content": "a"})
    client.post("/notes/", json={"title": "Cherry", "content": "c"})

    # Ascending sort by title
    r = client.get("/notes/", params={"sort": "title"})
    assert r.status_code == 200
    titles = [n["title"] for n in r.json()]
    assert titles == sorted(titles)

    # Descending sort by title
    r = client.get("/notes/", params={"sort": "-title"})
    assert r.status_code == 200
    titles = [n["title"] for n in r.json()]
    assert titles == sorted(titles, reverse=True)



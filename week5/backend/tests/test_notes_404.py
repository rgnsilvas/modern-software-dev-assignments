"""
Unit tests for 404 Not Found scenarios on notes endpoints.

Covers:
- GET  /notes/{note_id}  → 404 when the requested note does not exist
- Validates that the response body carries a meaningful error detail
- Confirms that a valid note ID still returns 200 (sanity check)
"""

NON_EXISTENT_ID = 99999


# ---------------------------------------------------------------------------
# GET /notes/{note_id}
# ---------------------------------------------------------------------------


def test_get_note_not_found(client):
    """Requesting a note that was never created returns 404."""
    r = client.get(f"/notes/{NON_EXISTENT_ID}")
    assert r.status_code == 404, r.text


def test_get_note_not_found_has_detail(client):
    """404 response body must include a 'detail' field with descriptive text."""
    r = client.get(f"/notes/{NON_EXISTENT_ID}")
    assert r.status_code == 404
    body = r.json()
    assert "detail" in body
    assert len(body["detail"]) > 0


def test_get_note_wrong_id_after_create(client):
    """After creating one note, requesting a different ID returns 404."""
    create_r = client.post("/notes/", json={"title": "Existing", "content": "Content"})
    assert create_r.status_code == 201
    created_id = create_r.json()["id"]

    wrong_id = created_id + 1
    r = client.get(f"/notes/{wrong_id}")
    assert r.status_code == 404, r.text


def test_get_note_zero_id_not_found(client):
    """ID 0 should never match a real note; expect 404."""
    r = client.get("/notes/0")
    assert r.status_code == 404, r.text


def test_get_note_negative_id_not_found(client):
    """Negative IDs are never assigned to notes; expect 404."""
    r = client.get("/notes/-1")
    assert r.status_code == 404, r.text


def test_get_note_not_found_after_listing_all(client):
    """
    Even when the database contains notes, an unknown ID still returns 404.
    """
    for i in range(3):
        client.post("/notes/", json={"title": f"Note {i}", "content": f"Body {i}"})

    r = client.get(f"/notes/{NON_EXISTENT_ID}")
    assert r.status_code == 404, r.text


# ---------------------------------------------------------------------------
# Sanity check – valid ID must NOT return 404
# ---------------------------------------------------------------------------


def test_get_existing_note_returns_200(client):
    """A note that exists must return 200, not 404 (guards against false positives)."""
    create_r = client.post("/notes/", json={"title": "Keep", "content": "This exists"})
    assert create_r.status_code == 201
    note_id = create_r.json()["id"]

    r = client.get(f"/notes/{note_id}")
    assert r.status_code == 200
    body = r.json()
    assert body["id"] == note_id
    assert body["title"] == "Keep"

import uuid


def create_report(client, **overrides):
    payload = {
        "description": "A deep pothole is blocking the left side of the road.",
        "location": "12 Market Street",
        **overrides,
    }
    return client.post("/api/reports", json=payload)


def test_create_and_get_report(client):
    created = create_report(client)
    assert created.status_code == 201
    body = created.json()
    uuid.UUID(body["id"])
    assert body["status"] == "reported"
    assert body["status_history"][0]["status"] == "reported"

    fetched = client.get(f"/api/reports/{body['id']}")
    assert fetched.status_code == 200
    assert fetched.json()["description"] == body["description"]


def test_list_search_and_filters(client):
    create_report(client, title="Broken light", category="streetlight", severity="high")
    create_report(client, title="Road damage", category="road", severity="medium")

    response = client.get("/api/reports", params={"search": "light", "category": "streetlight"})
    assert response.status_code == 200
    assert response.json()["total"] == 1
    assert response.json()["items"][0]["title"] == "Broken light"


def test_update_status_appends_history(client):
    report_id = create_report(client).json()["id"]
    response = client.patch(
        f"/api/reports/{report_id}/status",
        json={"status": "under_review", "note": "Location confirmed"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "under_review"
    assert [entry["status"] for entry in body["status_history"]] == ["reported", "under_review"]


def test_rejects_invalid_input_and_missing_report(client):
    assert create_report(client, description="short").status_code == 422
    assert client.get(f"/api/reports/{uuid.uuid4()}").status_code == 404


def test_resolved_report_cannot_be_reopened(client):
    report_id = create_report(client).json()["id"]
    assert client.patch(f"/api/reports/{report_id}/status", json={"status": "resolved"}).status_code == 200
    response = client.patch(f"/api/reports/{report_id}/status", json={"status": "in_progress"})
    assert response.status_code == 409


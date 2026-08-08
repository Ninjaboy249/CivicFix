import uuid


def create_report(client, **overrides):
    payload = {
        "title": "Deep pothole on Market Street",
        "description": "A deep pothole is blocking the left side of the road.",
        "category": "ROAD",
        "severity": "HIGH",
        "latitude": 28.6139,
        "longitude": 77.2090,
        **overrides,
    }
    return client.post("/api/reports", json=payload)


def test_create_report(client):
    created = create_report(client)
    assert created.status_code == 201
    body = created.json()
    uuid.UUID(body["id"])
    assert body["status"] == "REPORTED"
    assert body["category"] == "ROAD"
    assert body["latitude"] == 28.6139


def test_retrieve_reports(client):
    create_report(client)
    create_report(client, title="Broken streetlight", category="STREETLIGHT", severity="MEDIUM")

    response = client.get("/api/reports")

    assert response.status_code == 200
    assert len(response.json()) == 2


def test_filter_reports(client):
    create_report(client)
    create_report(client, title="Broken streetlight", category="STREETLIGHT", severity="MEDIUM")

    response = client.get(
        "/api/reports",
        params={"category": "STREETLIGHT", "severity": "MEDIUM", "status": "REPORTED"},
    )

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["category"] == "STREETLIGHT"


def test_retrieve_single_report(client):
    body = create_report(client).json()

    fetched = client.get(f"/api/reports/{body['id']}")
    assert fetched.status_code == 200
    assert fetched.json()["description"] == body["description"]


def test_update_report_status(client):
    report_id = create_report(client).json()["id"]
    response = client.patch(
        f"/api/reports/{report_id}/status",
        json={"status": "UNDER_REVIEW"},
    )
    assert response.status_code == 200
    assert response.json()["status"] == "UNDER_REVIEW"


def test_rejects_invalid_input_and_missing_report(client):
    assert create_report(client, description="short").status_code == 422
    assert create_report(client, latitude=91).status_code == 422
    assert client.get(f"/api/reports/{uuid.uuid4()}").status_code == 404


def test_rejects_invalid_category(client):
    response = create_report(client, category="PARKING")
    assert response.status_code == 422


def test_rejects_invalid_severity(client):
    response = create_report(client, severity="URGENT")
    assert response.status_code == 422


def test_coordinates_are_optional(client):
    response = create_report(client, latitude=None, longitude=None)
    assert response.status_code == 201
    assert response.json()["latitude"] is None
    assert response.json()["longitude"] is None


def test_resolved_report_cannot_be_reopened(client):
    report_id = create_report(client).json()["id"]
    assert client.patch(f"/api/reports/{report_id}/status", json={"status": "RESOLVED"}).status_code == 200
    response = client.patch(f"/api/reports/{report_id}/status", json={"status": "IN_PROGRESS"})
    assert response.status_code == 409

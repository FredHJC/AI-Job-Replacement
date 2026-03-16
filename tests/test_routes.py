from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_index_page():
    r = client.get("/")
    assert r.status_code == 200
    assert "/questionnaire" in r.text


def test_questionnaire_page():
    r = client.get("/questionnaire")
    assert r.status_code == 200
    assert "programmer" in r.text
    assert "filteredJobs" in r.text


def test_result_page():
    r = client.get("/result")
    assert r.status_code == 200


def test_score_api_valid():
    r = client.post("/api/score", json={
        "job_id": "programmer",
        "q2": "A", "q3": "A", "q4": "A", "q5": "A", "q6": "A", "q7": "A", "q8": "A",
    })
    assert r.status_code == 200
    data = r.json()
    assert data["total_score"] == 96
    assert data["risk_level"] == "extreme"


def test_score_api_invalid_option():
    r = client.post("/api/score", json={
        "job_id": "programmer",
        "q2": "X", "q3": "A", "q4": "A", "q5": "A", "q6": "A", "q7": "A", "q8": "A",
    })
    assert r.status_code == 422


def test_score_api_missing_field():
    r = client.post("/api/score", json={
        "job_id": "programmer",
        "q2": "A",
    })
    assert r.status_code == 422

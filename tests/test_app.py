import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "Programming Class" in data
    assert "Gym Class" in data

def test_signup_and_unregister():
    # Use a test email and activity
    test_email = "testuser@mergington.edu"
    activity = "Chess Club"

    # Sign up
    signup_resp = client.post(f"/activities/{activity}/signup?email={test_email}")
    assert signup_resp.status_code == 200
    assert "message" in signup_resp.json()

    # Check participant added
    activities = client.get("/activities").json()
    assert test_email in activities[activity]["participants"]

    # Unregister
    unregister_resp = client.post(f"/activities/{activity}/unregister?email={test_email}")
    assert unregister_resp.status_code == 200
    assert "message" in unregister_resp.json()

    # Check participant removed
    activities = client.get("/activities").json()
    assert test_email not in activities[activity]["participants"]

@pytest.mark.parametrize("activity", ["Chess Club", "Programming Class", "Gym Class"])
def test_signup_duplicate(activity):
    email = "duplicate@mergington.edu"
    # First signup
    client.post(f"/activities/{activity}/signup?email={email}")
    # Duplicate signup
    resp = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp.status_code == 400
    assert "already registered" in resp.json()["detail"].lower()
    # Cleanup
    client.post(f"/activities/{activity}/unregister?email={email}")

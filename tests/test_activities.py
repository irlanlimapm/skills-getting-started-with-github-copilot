def test_get_activities(client):
    response = client.get("/activities")

    assert response.status_code == 200
    activities = response.json()

    assert isinstance(activities, dict)
    assert "Chess Club" in activities
    assert "participants" in activities["Chess Club"]
    assert "michael@mergington.edu" in activities["Chess Club"]["participants"]


def test_signup_for_activity(client):
    response = client.post("/activities/Chess Club/signup", params={"email": "newstudent@mergington.edu"})

    assert response.status_code == 200
    assert response.json()["message"] == "Signed up newstudent@mergington.edu for Chess Club"

    activities = client.get("/activities").json()
    assert "newstudent@mergington.edu" in activities["Chess Club"]["participants"]


def test_signup_duplicate(client):
    response = client.post("/activities/Chess Club/signup", params={"email": "michael@mergington.edu"})

    assert response.status_code == 400
    assert response.json()["detail"] == "Student is already signed up for this activity"


def test_signup_unknown_activity(client):
    response = client.post("/activities/Unknown Activity/signup", params={"email": "student@mergington.edu"})

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_participant(client):
    response = client.delete("/activities/Chess Club/participants", params={"email": "michael@mergington.edu"})

    assert response.status_code == 200
    assert response.json()["message"] == "Unregistered michael@mergington.edu from Chess Club"

    activities = client.get("/activities").json()
    assert "michael@mergington.edu" not in activities["Chess Club"]["participants"]


def test_unregister_unknown_participant(client):
    response = client.delete("/activities/Chess Club/participants", params={"email": "notfound@mergington.edu"})

    assert response.status_code == 400
    assert response.json()["detail"] == "Participant not found in activity"


def test_root_redirect(client):
    response = client.get("/", follow_redirects=False)

    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"

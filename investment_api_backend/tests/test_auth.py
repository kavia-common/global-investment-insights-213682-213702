def test_signup_and_login_flow(client):
    # Signup
    resp = client.post("/auth/signup", json={"email": "user1@example.com", "password": "passw0rd", "full_name": "User One"})
    assert resp.status_code == 200, resp.text
    user = resp.json()
    assert user["email"] == "user1@example.com"
    assert user["is_active"] is True
    assert "id" in user

    # Duplicate signup should fail
    resp2 = client.post("/auth/signup", json={"email": "user1@example.com", "password": "passw0rd", "full_name": "User One"})
    assert resp2.status_code == 400

    # Login
    login = client.post("/auth/login", json={"email": "user1@example.com", "password": "passw0rd"})
    assert login.status_code == 200, login.text
    tok = login.json()
    assert "access_token" in tok

    # /me
    headers = {"Authorization": f"Bearer {tok['access_token']}"}
    me = client.get("/auth/me", headers=headers)
    assert me.status_code == 200
    me_json = me.json()
    assert me_json["email"] == "user1@example.com"


def test_login_wrong_password(client):
    client.post("/auth/signup", json={"email": "wrong@example.com", "password": "pass1word", "full_name": "X"})
    bad = client.post("/auth/login", json={"email": "wrong@example.com", "password": "nope"})
    assert bad.status_code == 400

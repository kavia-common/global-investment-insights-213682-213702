def test_onboarding_upsert(client, auth_headers_token):
    payload = {
        "experience_level": "beginner",
        "risk_tolerance": "low",
        "goals": "wealth_growth",
        "markets": "US,IN",
    }
    resp = client.post("/onboarding", json=payload, headers=auth_headers_token)
    assert resp.status_code == 200, resp.text
    data = resp.json()
    assert data["experience_level"] == "beginner"
    assert data["risk_tolerance"] == "low"
    assert data["markets"] == "US,IN"

    # Update
    payload2 = {**payload, "risk_tolerance": "medium"}
    resp2 = client.post("/onboarding", json=payload2, headers=auth_headers_token)
    assert resp2.status_code == 200
    assert resp2.json()["risk_tolerance"] == "medium"

def test_end_to_end_smoke_flow(client):
    # Register
    email = "smoke@example.com"
    password = "password123"
    reg = client.post("/auth/signup", json={"email": email, "password": password, "full_name": "Smoke"})
    assert reg.status_code in (200, 400), reg.text  # allow re-run

    # Login
    login = client.post("/auth/login", json={"email": email, "password": password})
    assert login.status_code == 200, login.text
    token = login.json().get("access_token")
    assert token

    headers = {"Authorization": f"Bearer {token}"}

    # Onboarding
    ob = client.post(
        "/onboarding",
        json={"experience_level": "beginner", "risk_tolerance": "low", "goals": "wealth", "markets": "US"},
        headers=headers,
    )
    assert ob.status_code == 200, ob.text

    # Suggestions generate once
    sug = client.post(
        "/suggestions",
        json={"symbol": "MSFT", "action": "buy", "rationale": "smoke", "target_price": 400.0, "market": "US"},
        headers=headers,
    )
    assert sug.status_code == 200, sug.text

    # Fetch suggestions list
    suglist = client.get("/suggestions", headers=headers)
    assert suglist.status_code == 200
    assert len(suglist.json().get("items", [])) >= 1

    # Portfolio get and add holding
    pf = client.get("/portfolio", headers=headers)
    assert pf.status_code == 200, pf.text

    add = client.post(
        "/portfolio/holdings",
        json={"symbol": "MSFT", "quantity": 5, "average_price": 300.0, "market": "US"},
        headers=headers,
    )
    assert add.status_code == 200, add.text

    pf2 = client.get("/portfolio", headers=headers)
    assert pf2.status_code == 200
    assert any(x["symbol"] == "MSFT" for x in pf2.json().get("holdings", []))

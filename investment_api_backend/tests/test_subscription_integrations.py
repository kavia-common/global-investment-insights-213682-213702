def test_subscription_upsert(client, auth_headers_token):
    resp = client.post("/subscription", json={"is_active": True, "plan": "monthly"}, headers=auth_headers_token)
    assert resp.status_code == 200, resp.text
    sub = resp.json()
    assert sub["is_active"] is True
    assert sub["plan"] == "monthly"


def test_integrations_upsert(client, auth_headers_token):
    payload = {"provider": "alpaca", "access_key": "key123"}
    resp = client.post("/integrations", json=payload, headers=auth_headers_token)
    assert resp.status_code == 200, resp.text
    integ = resp.json()
    assert integ["provider"] == "alpaca"
    assert integ["access_key"] == "key123"

def test_list_and_generate_suggestions(client, auth_headers_token):
    # Initially empty list
    list_resp = client.get("/suggestions", headers=auth_headers_token)
    assert list_resp.status_code == 200
    items = list_resp.json().get("items", [])
    assert isinstance(items, list)
    assert len(items) == 0

    # Create suggestion
    create_payload = {
        "symbol": "AAPL",
        "action": "buy",
        "rationale": "Test rationale",
        "target_price": 200.0,
        "market": "US",
    }
    create_resp = client.post("/suggestions", json=create_payload, headers=auth_headers_token)
    assert create_resp.status_code == 200, create_resp.text
    s = create_resp.json()
    assert s["symbol"] == "AAPL"
    assert s["action"] == "buy"
    assert s["market"] == "US"

    # List non-empty
    list_resp2 = client.get("/suggestions", headers=auth_headers_token)
    assert list_resp2.status_code == 200
    items2 = list_resp2.json().get("items", [])
    assert len(items2) >= 1

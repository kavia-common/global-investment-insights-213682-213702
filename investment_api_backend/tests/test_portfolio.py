def test_get_portfolio_and_upsert_holdings(client, auth_headers_token):
    # Get default portfolio (auto-created)
    resp = client.get("/portfolio", headers=auth_headers_token)
    assert resp.status_code == 200, resp.text
    pf = resp.json()
    assert pf["name"] == "Default"
    assert isinstance(pf["holdings"], list)
    assert pf["total_value"] == 0.0

    # Upsert a holding
    up = client.post(
        "/portfolio/holdings",
        json={"symbol": "AAPL", "quantity": 10, "average_price": 150.0, "market": "US"},
        headers=auth_headers_token,
    )
    assert up.status_code == 200, up.text
    h = up.json()
    assert h["symbol"] == "AAPL"
    assert h["quantity"] == 10

    # Portfolio should now include the holding
    pf2 = client.get("/portfolio", headers=auth_headers_token)
    assert pf2.status_code == 200
    holds = pf2.json()["holdings"]
    assert any(x["symbol"] == "AAPL" for x in holds)

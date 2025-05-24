import requests

def test_sync_logic_endpoint():
    response = requests.post("https://nova.novaaisecurity.com/sync-logic")
    assert response.status_code == 200
    assert "success" in response.json().get("status", "").lower()
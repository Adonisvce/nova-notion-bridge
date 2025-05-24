import requests

def test_sync_logic():
    response = requests.post("http://localhost:10000/sync-logic")
    assert response.status_code == 200
    assert response.json().get("status") == "success"

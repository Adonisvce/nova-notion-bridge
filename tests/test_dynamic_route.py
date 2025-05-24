import requests

def test_dynamic_logic_execution():
    payload = {
        "logic_name": "greet_user",
        "input": {"name": "Tester"}
    }
    response = requests.post("http://localhost:10000/dynamic", json=payload)
    assert response.status_code == 200
    assert "Hello, Tester" in response.json().get("result", "")

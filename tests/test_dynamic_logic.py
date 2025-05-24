import requests

def test_dynamic_logic_greet_user():
    response = requests.post(
        "https://nova.novaaisecurity.com/dynamic",
        json={"logic_name": "greet_user", "input": {"name": "Test"}}
    )
    assert response.status_code == 200
    assert "Hello, Test" in response.json().get("result", "")
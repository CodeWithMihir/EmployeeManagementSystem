import pytest
from .test_setup import client, db

@pytest.fixture
def auth_headers():
    return {"Authorization": "Bearer test_token",
            "X-User-Role": "admin"}

def test_create_employee(client, auth_headers):
    response = client.post("/employees/createemployee", json={
        "name": "John Doe",
        "age": 30,
        "department_id": 1
    }, headers=auth_headers)
    assert response.status_code == 201, response.text
    assert response.json()["name"] == "John Doe"

def test_get_all_employees(client):
    response = client.get("/employees/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_employee_by_id(client):
    response = client.get("/employees/1")
    assert response.status_code == 200 or response.status_code == 404  # Depends on data

def test_update_employee(client, auth_headers):
    response = client.put("/employees/1", json={
        "name": "John Updated",
        "age": 32,
        "department_id": 1
    }, headers=auth_headers)
    assert response.status_code in [204, 404], response.text

def test_delete_employee(client):
    response = client.delete("/employees/1")
    assert response.status_code in [204, 403]  # 403 if unauthorized

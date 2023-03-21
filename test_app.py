from fastapi import status
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


# Good example of func submit data
def test_submit_data():
    data = {
      "user_email": "user1@test.ru",
      "beauty_title": "Большой перевал",
      "title": "Перевал",
      "other_titles": "",
      "level_summer": 1,
      "level_autumn": 2,
      "level_winter": 5,
      "level_spring": 4,
      "connect": "connect",
      "add_time": "12.12.2022",
      "coord_id": 1
    }
    response = client.post("/submitData", json=data)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["status"] == "success"


# Bad example of func submit data - no coord_id data
def test_submit_data_not_coord_id_data():
    data = {
        "user_email": "user1@test.ru",
        "beauty_title": "Большой перевал",
        "title": "Перевал",
        "other_titles": "",
        "level_summer": 1,
        "level_autumn": 2,
    }
    response = client.post("/submitData", json=data)
    assert response.status_code == 422


# Bad example of func submit data - no user_email data
def test_submit_data_no_email():
    data = {
        "beauty_title": "Большой перевал",
        "title": "Перевал",
        "other_titles": "",
        "level_summer": 1,
        "level_autumn": 2,
        "coord_id": 1
    }
    response = client.post("/submitData", json=data)
    print(response.json())
    assert response.status_code == 422


# Bad example of func submit data - wrong email
def test_submit_data_invalid_email():
    data = {
        "user_email": "   ",
        "beauty_title": "Большой перевал",
        "title": "Перевал",
        "other_titles": "",
        "level_summer": 1,
        "level_autumn": 2,
        "coord_id": 1
    }
    response = client.post("/submitData", json=data)
    assert response.status_code == 200


# Bad example of post or update data - wrong kind of field (in this example - 'level_summer')
def test_wrong_data_type():
    data = {
      "user_email": "user1@test.ru",
      "level_summer": 'сложный',
      "coord_id": 1
    }
    response = client.post("/submitData", json=data)
    print(response.json())
    assert response.status_code == 422


# Goog example of get data of pereval by pereval_id
def test_get_pereval():
    response = client.get("/submitData/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == 1


# Bad example of get data of pereval by pereval_id - wrong pereval_id
def test_get_pereval_wrong_id():
    response = client.get("/submitData/00")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["state"] == 0


# Good example of get list of pereval by user_email
def test_get_user_perevals():
    response = client.get("/submitData/", params={"user_email": "user1@test.ru"})
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)


# Bad example of get list of pereval by user_email - wrong user_email
def test_get_user_perevals_wrong_email():
    response = client.get("/submitData/", params={"user_email": "wrong@test.ru"})
    assert response.status_code == 404


# Good example of patch (update) data of pereval by pereval_id
def test_update_pereval():
    data = {
        "title": "Перевал",
        "other_titles": "",
        "level_summer": 1,
        "level_autumn": 2
    }
    response = client.patch("/submitData/1", json=data)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["state"] == 1


# Bad example of patch (update) data of pereval by pereval_id - try to correct email
def test_update_pereval_use_email():
    data = {
        "user_email": "user1@test.ru",
    }
    response = client.patch("/submitData/1", json=data)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["state"] == 0


# Bad example of patch (update) data of pereval by pereval_id - wrong pereval_id
def test_update_pereval_wrong_id():
    data = {
        "level_summer": 1,
        "level_autumn": 2,
    }
    response = client.patch("/submitData/0", json=data)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["state"] == 0


import requests
from jsonschema import validate
from schemas import schema_create_user, schema_users_list, schema_register, schema_delay_response

url = 'https://reqres.in/api/users/'
name_user = 'Test'
job_user = 'QA'
email = 'eve.holt@reqres.in'
password = 'pistol'


def test_get_users():
    response = requests.get(url, params={'page': 2}, verify=False)
    body = response.json()
    validate(body, schema_users_list)
    assert response.status_code == 200


def test_update_user():
    data_user = {'name': name_user, 'job': job_user}
    response = requests.put(url + '2', data=data_user, verify=False)
    body = response.json()
    assert body['name'] == name_user
    assert body['job'] == job_user
    assert body['updatedAt'] != ''


def test_delete_user():
    response = requests.delete(url + '2', verify=False)
    assert response.text == ''
    assert response.status_code == 204


def test_return_valid_name_positive():
    data_user = {'name': name_user, 'job': job_user}
    response = requests.post(url, data=data_user, verify=False)
    body = response.json()
    assert body['name'] == name_user
    assert body['job'] == job_user
    assert response.status_code == 201


def test_return_valid_name_negative():
    data_user = {'name': name_user + 'negative', 'job': job_user + 'negative'}
    response = requests.post(url, data=data_user, verify=False)
    body = response.json()
    assert body['name'] != name_user
    assert body['job'] != job_user
    assert response.status_code == 201


def test_return_404():
    response = requests.get(url + '23234', verify=False)
    assert response.status_code == 404


def test_return_400():
    new_url = url.replace(("/users/"), "/register/")
    response = requests.post(new_url, verify=False)
    assert response.status_code == 400


def test_create_user_validate():
    data_user = {'name': name_user, 'job': job_user}
    response = requests.post(url, data=data_user, verify=False)
    body = response.json()
    validate(body, schema_create_user)
    assert response.status_code == 201


def test_register_schema_validate():
    data_user = {'email': email, 'password': password}
    new_url = url.replace(("/users/"), "/register/")
    response = requests.post(new_url, data=data_user, verify=False)
    body = response.json()
    validate(body, schema_register)


def test_delayed_schema_validate():
    response = requests.get(url, params='3', verify=False)
    body = response.json()
    validate(body, schema_delay_response)

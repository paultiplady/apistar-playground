from apistar.test import TestClient
from app import welcome, list_beer


def test_welcome():
    """
    Testing a view directly.
    """
    data = welcome()
    assert data == {'message': 'Welcome to API Star!'}


def test_http_request():
    """
    Testing a view, using the test client.
    """
    client = TestClient()
    response = client.get('http://localhost/')
    assert response.status_code == 200
    assert response.json() == {'message': 'Welcome to API Star!'}


def test_empty_list_beers():
    # beers = list_beer()
    # assert beers == []
    client = TestClient()
    response = client.get('/beers/')
    assert response.status_code == 200
    assert response.json() == {'beers': []}


def test_create_beer():
    client = TestClient()
    create_response = client.post('/beers/', json={'name': 'My first'})
    assert create_response.status_code == 200

    list_response = client.get('/beers/')
    assert list_response.status_code == 200
    assert list_response.json() == {'beers': [{'name': 'My first'}]}

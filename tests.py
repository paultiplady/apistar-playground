import pytest
from apistar.backends import SQLAlchemy
from apistar.test import TestClient

from app import welcome, app


@pytest.fixture
def reset_db(scope="function"):
    db_backend = SQLAlchemy.build(app.settings)
    db_backend.drop_tables()
    db_backend.create_tables()


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


def test_empty_list_beers(reset_db):
    client = TestClient()
    response = client.get('/beers/')
    assert response.status_code == 200
    assert response.json() == {'beers': []}


def test_create_beer(reset_db):
    client = TestClient()
    create_response = client.post('/beers/', json={'name': 'My first'})
    assert create_response.status_code == 200

    list_response = client.get('/beers/')
    assert list_response.status_code == 200
    assert list_response.json() == {'beers': [{'name': 'My first'}]}

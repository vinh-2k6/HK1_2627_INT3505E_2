import pytest
from app import app, db

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_get_books_offset(client):
    res = client.get('/api/v1/books?strategy=offset&limit=2')
    assert res.status_code == 200
    assert res.json['strategy'] == 'offset'

def test_get_books_cursor(client):
    res = client.get('/api/v1/books?strategy=cursor&limit=2')
    assert res.status_code == 200
    assert res.json['strategy'] == 'cursor'

def test_get_books_filter_genre(client):
    res = client.get('/api/v1/books?genre=fiction')
    assert res.status_code == 200
    for book in res.json['data']:
        assert book['category']['slug'] == 'fiction'
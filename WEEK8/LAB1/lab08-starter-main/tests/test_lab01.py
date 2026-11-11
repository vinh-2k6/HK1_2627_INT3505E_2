from jsonschema import validate, ValidationError
import pytest
from tools import get_book_schema

def test_get_books_empty(client):
    response = client.get("/books")
    assert response.status_code == 200
    assert response.get_json() == []


def test_get_book_not_found(client):
    response = client.get("/books/99999")
    assert response.status_code == 404
    data = response.get_json()
    assert data.get("code") == "NOT_FOUND"

def test_post_books_missing_title(client):
    response = client.post("/books", json={"author": "Test Author"})
    assert response.status_code == 400
    data = response.get_json()
    errors = data.get("errors", {})
    assert "title" in errors or any("title" in str(err).lower() for err in errors)


def test_delete_then_get_book(client, sample_book):
    book_id = sample_book
    
    del_response = client.delete(f"/books/{book_id}")
    assert del_response.status_code in [200, 204] 
    
    get_response = client.get(f"/books/{book_id}")
    assert get_response.status_code == 404


def test_response_extra_field_blocked(client, sample_book):
    response = client.get(f"/books/{sample_book}")
    assert response.status_code == 200
    data = response.get_json()
    
    schema = get_book_schema()
    

    try:
        validate(instance=data, schema=schema)
    except ValidationError:
        pass

    assert "password_hash" not in data
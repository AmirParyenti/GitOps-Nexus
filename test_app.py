# test_app.py
import pytest # type: ignore
from app import app, get_db_connection
from unittest.mock import patch, MagicMock

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def mock_db_conn(mocker):
    mock_conn = MagicMock()
    mock_cur = MagicMock()
    mock_conn.cursor.return_value = mock_cur
    mock_cur.fetchall.return_value = [
        {'name': 'John', 'second_name': 'Doe', 'age': 30, 'id_number': '123', 'city': 'New York'}
    ]
    mocker.patch('psycopg2.connect', return_value=mock_conn)
    return mock_conn, mock_cur

def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Input Form' in response.data

def test_submit(client, mock_db_conn):
    response = client.post('/submit', data={
        'name': 'Jane',
        'second_name': 'Doe',
        'age': 25,
        'id_number': '456',
        'city': 'Los Angeles'
    })
    assert response.status_code == 200
    assert b'User added successfully' in response.data
    mock_conn, mock_cur = mock_db_conn
    mock_cur.execute.assert_called_once()
    mock_conn.commit.assert_called_once()

def test_search(client, mock_db_conn):
    response = client.post('/search', data={'search_name': 'John'})
    assert response.status_code == 200
    assert b'John' in response.data
    assert b'New York' in response.data
    mock_conn, mock_cur = mock_db_conn
    mock_cur.execute.assert_called_once_with('SELECT * FROM users WHERE name = %s', ('John',))

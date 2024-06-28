import pytest
from app import create_app
from app.extensions.db import db as _db

@pytest.fixture(scope='session')
def app():
    app = create_app('testing')
    with app.app_context():
        yield app

@pytest.fixture(scope='session')
def client(app):
    return app.test_client()

@pytest.fixture(scope='session')
def db(app):
    _db.app = app
    with app.app_context():
        _db.create_all()
        yield _db
        _db.drop_all()
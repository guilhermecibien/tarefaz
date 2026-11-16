import os
import tempfile

import pytest

from app import create_app
from app.models.database import init_db


@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()
    application = create_app({"TESTING": True, "DATABASE": db_path, "SECRET_KEY": "teste"})
    with application.app_context():
        init_db()
    yield application
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    return app.test_client()


def register(client, name="Maria", email="maria@email.com", password="senha123"):
    return client.post("/cadastro", data={"nome": name, "email": email, "senha": password}, follow_redirects=True)


def login(client, email="maria@email.com", password="senha123"):
    return client.post("/login", data={"email": email, "senha": password}, follow_redirects=True)

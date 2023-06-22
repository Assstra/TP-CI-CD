"""Module for test configurations."""
import os
import sys
import pytest

current = os.path.dirname(os.path.realpath(__file__))
parent_directory = os.path.dirname(current)

sys.path.append(parent_directory)

from application import app as flask_app

@pytest.fixture
def app():
    """Function creating an app fixture for tests."""
    yield flask_app


@pytest.fixture
def client(app):
    """Function creating a client fixture for tests."""
    return app.test_client()

# tests/conftest.py
import pytest
from starlette.testclient import TestClient
from clases.global_session import global_session  # Import your app or endpoints
from unittest.mock import Mock
from starlette.routing import Mount, Route
from starlette.applications import Starlette
from auth.validate import ValidateTokenEndpoint
from api.api_manager import *
from api.login import LoginEndpoint, LoginStarletteSessionEndpoint
    

@pytest.fixture
def test_client():
    app = Starlette(routes=[
        Route('/validate-token', ValidateTokenEndpoint),
        Route('/login', LoginEndpoint),
        Route('/login-session', LoginStarletteSessionEndpoint),
    ])
    return TestClient(app)

@pytest.fixture
def mock_session():
    session = Mock()
    session.session_state = {"is_logged_in": False, "id": None}
    return session

@pytest.fixture
def mock_global_session():
    return global_session  # Use the real global_session, but we'll mock its methods
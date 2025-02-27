# tests/test_api.py
import pytest
import json
from starlette.requests import Request
from unittest.mock import patch, Mock

# Import your endpoints
from auth.validate import ValidateTokenEndpoint
from api.login import LoginEndpoint, LoginStarletteSessionEndpoint

@pytest.mark.asyncio
async def test_validate_token_success(test_client, mocker):
    """Test successful token validation redirects to /shiny"""
    # Mock httpx AsyncClient to simulate a successful Auth0 response
    mock_client = mocker.patch('httpx.AsyncClient')
    mock_response = Mock()
    mock_response.status_code = 200
    mock_client.return_value.__aenter__.return_value.get.return_value = mock_response
    
    # Send POST request to /validate-token
    response = test_client.post(
        '/validate-token',
        json={"access_token": "valid_token"}
    )
    
    # Assertions
    assert response.status_code == 200
    assert response.json() == {"redirect_url": "http://localhost:3000/shiny/"}
    mock_client.return_value.__aenter__.return_value.get.assert_called_once_with(
        f"https://your-auth0-domain/userinfo",
        headers={"Authorization": "Bearer valid_token"}
    )

@pytest.mark.asyncio
async def test_validate_token_missing(test_client):
    """Test missing token returns 401"""
    # Send POST request with no token
    response = test_client.post('/validate-token', json={})
    
    # Assertions
    assert response.status_code == 401
    assert response.json() == {"error": "Token no proporcionado"}

@pytest.mark.asyncio
async def test_validate_token_invalid(test_client, mocker):
    """Test invalid token returns 401"""
    # Mock httpx to simulate an invalid token response
    mock_client = mocker.patch('httpx.AsyncClient')
    mock_response = Mock()
    mock_response.status_code = 401
    mock_client.return_value.__aenter__.return_value.get.return_value = mock_response
    
    # Send POST request
    response = test_client.post('/validate-token', json={"access_token": "invalid_token"})
    
    # Assertions
    assert response.status_code == 401
    assert response.json() == {"error": "Token inválido"}

@pytest.mark.asyncio
async def test_login_endpoint_success(test_client, mocker):
    """Test successful login sets session and returns user_id"""
    # Mock helper functions
    mock_obtener_token = mocker.patch('api.login.obtener_token', return_value="valid_token")
    mock_obtener_user_info = mocker.patch('api.login.obtener_user_info', return_value={"sub": "user|123"})
    
    # Send POST request to /login
    response = test_client.post(
        '/login',
        json={"username": "testuser", "password": "testpass"}
    )
    
    # Assertions
    assert response.status_code == 200
    assert response.json() == {"message": "Login exitoso", "user_id": "user_123"}
    mock_obtener_token.assert_called_once()
    mock_obtener_user_info.assert_called_once_with("valid_token", mocker.ANY)  # configuration is passed as ANY

@pytest.mark.asyncio
async def test_login_endpoint_no_token(test_client, mocker):
    """Test login fails when no token is returned"""
    # Mock obtener_token to return None
    mocker.patch('api.login.obtener_token', return_value=None)
    
    # Send POST request
    response = test_client.post('/login', json={"username": "testuser", "password": "testpass"})
    
    # Assertions
    assert response.status_code == 401
    assert response.json() == {"error": "No se recibió el token de acceso."}

@pytest.mark.asyncio
async def test_login_starlette_session_success(test_client):
    """Test successful session update with user_id"""
    # Send POST request to /login-session
    response = test_client.post('/login-session', json={"user_id": "user_123"})
    
    # Assertions
    assert response.status_code == 200
    assert response.json() == {"message": "Starlette session updated."}
    # Check session (test_client maintains session state)
    assert test_client.cookies.get("session") is not None  # Session is set, though exact value depends on Starlette's session middleware

@pytest.mark.asyncio
async def test_login_starlette_session_missing_user_id(test_client):
    """Test missing user_id returns 400"""
    # Send POST request with no user_id
    response = test_client.post('/login-session', json={})
    
    # Assertions
    assert response.status_code == 400
    assert response.json() == {"error": "Falta user_id"}
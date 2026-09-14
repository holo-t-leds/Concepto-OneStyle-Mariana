import pytest
from src.auth.service import AuthService

@pytest.fixture
def auth():
    return AuthService()

def test_registrar_cliente_exito(auth):
    user_id = auth.registrar_cliente("Ana", "Gomez", "ana@example.com", "securepwd123")
    assert user_id == 1
    assert auth.usuarios[user_id]['email'] == "ana@example.com"
    assert auth.usuarios[user_id]['rol'] == "Clienta"

def test_registrar_cliente_contrasena_corta(auth):
    with pytest.raises(ValueError, match="al menos 8 caracteres"):
        auth.registrar_cliente("Ana", "Gomez", "ana@example.com", "short")

def test_registrar_cliente_email_duplicado(auth):
    auth.registrar_cliente("Ana", "Gomez", "ana@example.com", "securepwd123")

    with pytest.raises(ValueError, match="ya está registrado"):
        auth.registrar_cliente("Otra", "Ana", "ana@example.com", "anotherpwd")

def test_validar_credenciales_exito(auth):
    auth.registrar_cliente("Ana", "Gomez", "ana@example.com", "securepwd123")
    token = auth.validar_credenciales("ana@example.com", "securepwd123")

    assert token is not None
    assert auth.verificar_sesion(token) is True

def test_validar_credenciales_fallo(auth):
    auth.registrar_cliente("Ana", "Gomez", "ana@example.com", "securepwd123")

    with pytest.raises(ValueError, match="Credenciales inválidas"):
        auth.validar_credenciales("ana@example.com", "wrongpwd")

    with pytest.raises(ValueError, match="Credenciales inválidas"):
         auth.validar_credenciales("nonexistent@example.com", "securepwd123")

def test_get_user_role(auth):
    auth.registrar_cliente("Ana", "Gomez", "ana@example.com", "securepwd123")
    token = auth.validar_credenciales("ana@example.com", "securepwd123")

    role = auth.get_user_role(token)
    assert role == "Clienta"

def test_get_user_role_token_invalido(auth):
    with pytest.raises(ValueError, match="Sesión inválida o expirada"):
        auth.get_user_role("invalid-token")

from datetime import datetime, timedelta

def test_recuperacion_token_ttl(auth):
    user_id = auth.registrar_cliente("Ana", "Gomez", "ana@example.com", "securepwd123")
    token = auth.solicitar_recuperacion("ana@example.com")

    assert token is not None
    assert auth.usuarios[user_id]['reset_token_hash'] is not None
    assert auth.usuarios[user_id]['reset_token_expira'] is not None

    # Check TTL is around 15 minutes
    expira = auth.usuarios[user_id]['reset_token_expira']
    expected_expira = datetime.now() + timedelta(minutes=15)

    # Compare timestamps allowing a tiny margin of error (seconds)
    delta = abs((expira - expected_expira).total_seconds())
    assert delta < 5

def test_rechazo_token_vencido(auth):
    user_id = auth.registrar_cliente("Ana", "Gomez", "ana@example.com", "securepwd123")
    token = auth.solicitar_recuperacion("ana@example.com")

    # Simulate expiration by rolling back the expiration time to the past
    auth.usuarios[user_id]['reset_token_expira'] = datetime.now() - timedelta(minutes=1)

    with pytest.raises(ValueError, match="El token de recuperación ha expirado"):
        auth.restablecer_password(token, "new_secure_pwd")

def test_invalidacion_inmediata_token(auth):
    user_id = auth.registrar_cliente("Ana", "Gomez", "ana@example.com", "securepwd123")
    token = auth.solicitar_recuperacion("ana@example.com")

    # Reset password successfully
    result = auth.restablecer_password(token, "new_secure_pwd")
    assert result is True

    # Validate the token hash and expiration are immediately cleared
    assert auth.usuarios[user_id]['reset_token_hash'] is None
    assert auth.usuarios[user_id]['reset_token_expira'] is None

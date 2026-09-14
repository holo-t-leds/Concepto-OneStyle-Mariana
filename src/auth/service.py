# src/auth/service.py
import hashlib
import uuid
from datetime import datetime, timedelta

class AuthService:
    def __init__(self):
        # mock DB for users
        self.usuarios = {} # id: {'email': str, 'pwd_hash': str, 'rol': str}
        self.sesiones = {} # token: {'user_id': int, 'expires_at': datetime}
        self.user_id_counter = 1

    def _hash_password(self, password: str) -> str:
        # Simplistic hash for demo purposes. Real systems should use bcrypt/argon2.
        return hashlib.sha256(password.encode()).hexdigest()

    def registrar_cliente(self, nombre: str, apellido: str, email: str, contrasena: str):
        # Validación de contraseña simple
        if len(contrasena) < 8:
            raise ValueError("La contraseña debe tener al menos 8 caracteres.")

        for user in self.usuarios.values():
            if user['email'] == email:
                raise ValueError("El correo electrónico ya está registrado.")

        user_id = self.user_id_counter
        self.usuarios[user_id] = {
            'nombre': nombre,
            'apellido': apellido,
            'email': email,
            'pwd_hash': self._hash_password(contrasena),
            'rol': 'Clienta',
            'google_id': None,
            'reset_token_hash': None,
            'reset_token_expira': None
        }
        self.user_id_counter += 1
        return user_id

    def validar_credenciales(self, email: str, contrasena: str) -> str:
        for user_id, user_data in self.usuarios.items():
            if user_data['email'] == email and user_data['pwd_hash'] == self._hash_password(contrasena):
                # Generar token de sesión
                token = str(uuid.uuid4())
                self.sesiones[token] = {
                    'user_id': user_id,
                    'expires_at': datetime.now() + timedelta(hours=1)
                }
                return token

        raise ValueError("Credenciales inválidas.")

    def verificar_sesion(self, token: str) -> bool:
        if token in self.sesiones:
            if datetime.now() < self.sesiones[token]['expires_at']:
                return True
            else:
                del self.sesiones[token]
        return False

    def get_user_role(self, token: str) -> str:
        if not self.verificar_sesion(token):
             raise ValueError("Sesión inválida o expirada.")

        user_id = self.sesiones[token]['user_id']
        return self.usuarios[user_id]['rol']

    def google_oauth_verify(self, id_token: str) -> dict:
        """
        Stub function to verify Google OAuth token.
        In a real application, this would use google-auth or similar.
        Returns mock user data.
        """
        if not id_token or id_token == "invalid":
            raise ValueError("Token de Google inválido.")

        return {
            "email": "test@gmail.com",
            "google_id": "google123456",
            "nombre": "Test",
            "apellido": "Google"
        }

    def solicitar_recuperacion(self, email: str) -> str:
        """
        Genera un token de recuperación y simula la preparación del email transaccional.
        """
        user_id = None
        for uid, user in self.usuarios.items():
            if user['email'] == email:
                user_id = uid
                break

        if not user_id:
            raise ValueError("El correo electrónico no está registrado.")

        token = str(uuid.uuid4())
        token_hash = hashlib.sha256(token.encode()).hexdigest()

        self.usuarios[user_id]['reset_token_hash'] = token_hash
        self.usuarios[user_id]['reset_token_expira'] = datetime.now() + timedelta(minutes=15)

        # Simula la llamada a la API de Resend u otra
        # print(f"Preparando envío de correo a {email} con token {token}")

        return token

    def restablecer_password(self, token: str, nueva_password: str):
        """
        Valida el token de recuperación y establece la nueva contraseña.
        """
        if len(nueva_password) < 8:
            raise ValueError("La nueva contraseña debe tener al menos 8 caracteres.")

        token_hash = hashlib.sha256(token.encode()).hexdigest()

        for user_id, user_data in self.usuarios.items():
            if user_data.get('reset_token_hash') == token_hash:
                if datetime.now() > user_data['reset_token_expira']:
                    self.usuarios[user_id]['reset_token_hash'] = None
                    self.usuarios[user_id]['reset_token_expira'] = None
                    raise ValueError("El token de recuperación ha expirado.")

                # Update password
                self.usuarios[user_id]['pwd_hash'] = self._hash_password(nueva_password)
                # Invalidate token immediately
                self.usuarios[user_id]['reset_token_hash'] = None
                self.usuarios[user_id]['reset_token_expira'] = None
                return True

        raise ValueError("Token de recuperación inválido.")

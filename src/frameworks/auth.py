"""
Ludwig Authentication System

Laravel-inspired authentication with JWT tokens, password hashing,
and user session management.
"""

import hashlib
import hmac
import base64
import json
import secrets
import time
from datetime import datetime, timedelta
from database import User, Database


class PasswordHasher:
    """Secure password hashing using PBKDF2."""
    
    @staticmethod
    def hash(password, salt=None):
        """Hash a password with salt."""
        if salt is None:
            salt = secrets.token_hex(16)
        
        # Use PBKDF2 with SHA256
        hashed = hashlib.pbkdf2_hmac('sha256', 
                                   password.encode('utf-8'), 
                                   salt.encode('utf-8'), 
                                   100000)  # 100k iterations
        
        return f"{salt}:{base64.b64encode(hashed).decode('utf-8')}"
    
    @staticmethod
    def verify(password, hashed_password):
        """Verify a password against its hash."""
        try:
            salt, stored_hash = hashed_password.split(':')
            
            # Hash the provided password with the stored salt
            new_hash = hashlib.pbkdf2_hmac('sha256',
                                         password.encode('utf-8'),
                                         salt.encode('utf-8'),
                                         100000)
            
            new_hash_b64 = base64.b64encode(new_hash).decode('utf-8')
            
            # Constant-time comparison to prevent timing attacks
            return hmac.compare_digest(stored_hash, new_hash_b64)
        except (ValueError, KeyError) as e:
            return False


class JWTToken:
    """Simple JWT token implementation."""
    
    def __init__(self, secret_key="ludwig_secret_key_change_in_production"):
        """Initialize JWT handler."""
        self.secret_key = secret_key.encode('utf-8')
    
    def encode(self, payload, expiry_hours=24):
        """Encode a JWT token."""
        # Header
        header = {
            "typ": "JWT",
            "alg": "HS256"
        }
        
        # Payload with expiration
        now = datetime.utcnow()
        payload.update({
            "iat": int(now.timestamp()),
            "exp": int((now + timedelta(hours=expiry_hours)).timestamp())
        })
        
        # Encode components
        header_b64 = base64.urlsafe_b64encode(
            json.dumps(header, separators=(',', ':')).encode('utf-8')
        ).decode('utf-8').rstrip('=')
        
        payload_b64 = base64.urlsafe_b64encode(
            json.dumps(payload, separators=(',', ':')).encode('utf-8')
        ).decode('utf-8').rstrip('=')
        
        # Create signature
        message = f"{header_b64}.{payload_b64}".encode('utf-8')
        signature = hmac.new(self.secret_key, message, hashlib.sha256).digest()
        signature_b64 = base64.urlsafe_b64encode(signature).decode('utf-8').rstrip('=')
        
        return f"{header_b64}.{payload_b64}.{signature_b64}"
    
    def decode(self, token):
        """Decode and verify a JWT token."""
        try:
            header_b64, payload_b64, signature_b64 = token.split('.')
            
            # Verify signature
            message = f"{header_b64}.{payload_b64}".encode('utf-8')
            expected_signature = hmac.new(self.secret_key, message, hashlib.sha256).digest()
            expected_signature_b64 = base64.urlsafe_b64encode(expected_signature).decode('utf-8').rstrip('=')
            
            if not hmac.compare_digest(signature_b64, expected_signature_b64):
                return None
            
            # Decode payload
            payload_padded = payload_b64 + '=' * (4 - len(payload_b64) % 4)
            payload = json.loads(base64.urlsafe_b64decode(payload_padded))
            
            # Check expiration
            if payload.get('exp', 0) < time.time():
                return None
            
            return payload
        
        except (ValueError, KeyError) as e:
            return None


class Auth:
    """Main authentication class."""
    
    def __init__(self):
        """Initialize authentication."""
        self.jwt = JWTToken()
        self.current_user = None
    
    def register(self, name, email, password):
        """Register a new user."""
        # Check if user already exists
        existing_user = User.where('email', email).first()
        if existing_user:
            return {'success': False, 'message': 'Email already registered'}
        
        # Hash password
        hashed_password = PasswordHasher.hash(password)
        
        # Create user
        try:
            user = User.create({
                'name': name,
                'email': email,
                'password': hashed_password,
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat()
            })
            
            return {
                'success': True,
                'user': {
                    'id': user.id,
                    'name': user.name,
                    'email': user.email
                },
                'message': 'User registered successfully'
            }
        
        except Exception as e:
            return {'success': False, 'message': f'Registration failed: {str(e)}'}
    
    def login(self, email, password):
        """Authenticate user and return token."""
        # Find user
        user = User.where('email', email).first()
        if not user:
            return {'success': False, 'message': 'Invalid credentials'}
        
        # Verify password
        if not PasswordHasher.verify(password, user.password):
            return {'success': False, 'message': 'Invalid credentials'}
        
        # Generate token
        token = self.jwt.encode({
            'user_id': user.id,
            'email': user.email,
            'name': user.name
        })
        
        return {
            'success': True,
            'token': token,
            'user': {
                'id': user.id,
                'name': user.name,
                'email': user.email
            },
            'message': 'Login successful'
        }
    
    def verify_token(self, token):
        """Verify JWT token and return user data."""
        payload = self.jwt.decode(token)
        if not payload:
            return None
        
        # Get fresh user data
        user = User.find(payload['user_id'])
        if not user:
            return None
        
        return {
            'id': user.id,
            'name': user.name,
            'email': user.email
        }
    
    def get_user_from_token(self, token):
        """Get User model instance from token."""
        payload = self.jwt.decode(token)
        if not payload:
            return None
        
        return User.find(payload['user_id'])
    
    def middleware(self, request):
        """Authentication middleware for web requests."""
        # Get token from Authorization header or cookie
        auth_header = request.get('headers', {}).get('Authorization', '')
        
        if auth_header.startswith('Bearer '):
            token = auth_header[7:]  # Remove 'Bearer ' prefix
        else:
            # Check for cookie-based auth
            token = request.get('cookies', {}).get('auth_token')
        
        if not token:
            return {'authenticated': False, 'user': None}
        
        user_data = self.verify_token(token)
        if user_data:
            self.current_user = user_data
            return {'authenticated': True, 'user': user_data}
        
        return {'authenticated': False, 'user': None}
    
    def logout(self):
        """Logout current user."""
        self.current_user = None
        return {'success': True, 'message': 'Logged out successfully'}
    
    def user(self):
        """Get current authenticated user."""
        return self.current_user
    
    def check(self):
        """Check if user is authenticated."""
        return self.current_user is not None
    
    def guest(self):
        """Check if user is a guest (not authenticated)."""
        return self.current_user is None


class AuthMiddleware:
    """Authentication middleware for Ludwig web framework."""
    
    def __init__(self):
        """Initialize auth middleware."""
        self.auth = Auth()
    
    def handle(self, request, next_handler):
        """Handle authentication for requests."""
        # Perform authentication
        auth_result = self.auth.middleware(request)
        
        # Add auth info to request
        request['auth'] = auth_result
        request['user'] = auth_result['user']
        
        # Continue to next handler
        return next_handler(request)


class GuestMiddleware:
    """Middleware for guest-only routes (login, register)."""
    
    def __init__(self):
        """Initialize guest middleware."""
        self.auth = Auth()
    
    def handle(self, request, next_handler):
        """Handle guest-only routes."""
        auth_result = self.auth.middleware(request)
        
        if auth_result['authenticated']:
            # Redirect authenticated users away from guest routes
            return {
                'status': 302,
                'redirect': '/dashboard',
                'message': 'Already authenticated'
            }
        
        return next_handler(request)


class ProtectedMiddleware:
    """Middleware for protected routes."""
    
    def __init__(self):
        """Initialize protected middleware."""
        self.auth = Auth()
    
    def handle(self, request, next_handler):
        """Handle protected routes."""
        auth_result = self.auth.middleware(request)
        
        if not auth_result['authenticated']:
            # Redirect unauthenticated users to login
            return {
                'status': 302,
                'redirect': '/login',
                'message': 'Authentication required'
            }
        
        # Add auth info to request
        request['auth'] = auth_result
        request['user'] = auth_result['user']
        
        return next_handler(request)


# Helper functions for Ludwig
def auth():
    """Get global auth instance."""
    if not hasattr(auth, '_instance'):
        auth._instance = Auth()
    return auth._instance


def hash_password(password):
    """Hash a password."""
    return PasswordHasher.hash(password)


def verify_password(password, hashed):
    """Verify a password."""
    return PasswordHasher.verify(password, hashed)


# Example usage and testing
if __name__ == "__main__":
    # Initialize database and auth
    from database import create_users_table
    
    db = Database()
    create_users_table(db)
    
    auth_system = Auth()
    
    # Test registration
    reg_result = auth_system.register(
        "John Doe",
        "john@example.com", 
        "secure_password123"
    )
    print("Registration:", reg_result)
    
    # Test login
    login_result = auth_system.login("john@example.com", "secure_password123")
    print("Login:", login_result)
    
    if login_result['success']:
        token = login_result['token']
        print(f"Token: {token[:50]}...")
        
        # Test token verification
        user_data = auth_system.verify_token(token)
        print("Token verification:", user_data)
    
    # Test wrong password
    wrong_login = auth_system.login("john@example.com", "wrong_password")
    print("Wrong password:", wrong_login)
    
    db.close()

from django.conf import settings
from datetime import datetime, timedelta
import jwt

def generate_access_token(user):
    payload = {
        'id': user.id,
        'exp': datetime.utcnow() + timedelta(days=1, minutes=0),
        'iat': datetime.utcnow(),
    }

    access_token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    return access_token

def generate_mock_response(message):
    """Generates a simple mock response based on the input message."""
    response = f"Thanks for your message: {message}. Here's a mock response!"
    return response

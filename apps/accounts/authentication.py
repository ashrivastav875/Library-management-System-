"""
Custom JWT authentication that works with or without 'Bearer' prefix.
"""
from rest_framework_simplejwt.authentication import JWTAuthentication


class FlexibleJWTAuthentication(JWTAuthentication):
    """
    JWT authentication that accepts tokens with or without 'Bearer' prefix.
    
    Accepts:
    - Authorization: Bearer <token>
    - Authorization: <token>
    """
    
    def get_header(self, request):
        """Get the Authorization header and auto-add 'Bearer ' if missing."""
        header = super().get_header(request)
        
        if header and not header.startswith(b'Bearer '):
            # Token provided without 'Bearer' prefix - add it
            header = b'Bearer ' + header
        
        return header
